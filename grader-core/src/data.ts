// Dataset resolution and the hidden-check data mutations. Mirrors scripts/checkers/dataset.py + sandbox.py apply_ops exactly.
export type Column = { name: string; type?: string };
export type Table = { name: string; columns: Column[]; rows: unknown[][] };
export type Registry = { assets: any[] };

const matches = (row: Record<string, unknown>, where: Record<string, unknown>) => Object.entries(where).every(([k, v]) => row[k] === v);
const findRow = (rows: Record<string, unknown>[], where: Record<string, unknown>, occurrence = 0) => {
  const hits = rows.flatMap((r, i) => (matches(r, where) ? [i] : []));
  return hits[occurrence] ?? null;
};
const clone = <T>(x: T): T => JSON.parse(JSON.stringify(x));

export function resolveDataset(reg: Registry, assetId: string, variantId?: string | null) {
  const ds = reg.assets.find((a) => a.asset_id === assetId);
  if (!ds || ds.asset_kind !== "dataset") throw new Error(`no dataset asset ${assetId}`);
  if (!ds.rows) throw new Error(`${assetId}: data_file datasets are resolved by the runtime, not inline`);
  const names: string[] = ds.columns.map((c: Column) => c.name);
  let cols: Column[] = clone(ds.columns);
  let rows: Record<string, unknown>[] = ds.rows.map((r: unknown[]) => Object.fromEntries(names.map((n, i) => [n, r[i]])));
  if (!variantId) return { columns: cols, rows };
  const variants: Record<string, any> = Object.fromEntries((ds.variants ?? []).map((v: any) => [v.variant_id, v]));
  if (!variants[variantId]) throw new Error(`${assetId}: no variant ${variantId}`);
  const chain: any[] = [];
  for (let cur = variants[variantId]; ; cur = variants[cur.derived_from]) {
    chain.push(cur);
    if (cur.derived_from === "base" || cur.derived_from === assetId) break;
  }
  for (const v of chain.reverse()) for (const op of v.ops) {
    if (op.op === "set_cell") {
      const i = findRow(rows, op.where, op.occurrence ?? 0);
      if (i === null) throw new Error(`${variantId}: set_cell matched no row`);
      rows[i][op.column] = op.value;
    } else if (op.op === "duplicate_row") {
      const i = findRow(rows, op.where, op.occurrence ?? 0);
      if (i === null) throw new Error(`${variantId}: duplicate_row matched no row`);
      rows.splice(op.insert === "end" ? rows.length : i + 1, 0, { ...rows[i] });
    } else if (op.op === "drop_rows") rows = rows.filter((r) => !matches(r, op.where));
    else if (op.op === "drop_columns") {
      cols = cols.filter((c) => !op.columns.includes(c.name));
      rows = rows.map((r) => Object.fromEntries(Object.entries(r).filter(([k]) => !op.columns.includes(k))));
    }
  }
  return { columns: cols, rows };
}

/** The tables an exercise mounts, as {name: mount_path, columns, rows[][]}. `overrides` maps mount_path -> variant_id (a test's mount_variants). */
export function mountTables(reg: Registry, mounts: any[], overrides: Record<string, string> = {}): Table[] {
  return mounts.map((m) => {
    const { columns, rows } = resolveDataset(reg, m.asset_id, overrides[m.mount_path] ?? m.variant_id);
    const names = columns.map((c) => c.name);
    return { name: m.mount_path, columns: columns.map((c) => ({ name: c.name, type: c.type ?? "string" })), rows: rows.map((r) => names.map((n) => r[n])) };
  });
}

/** drop_row{index} | duplicate_row{index} | set_cell{index, column, value}: returns a mutated deep copy. */
export function applyOps(table: Table, ops: any[]): Table {
  const t = clone(table), names = t.columns.map((c) => c.name);
  for (const o of ops) {
    const i = o.index;
    if (o.op === "drop_row" && i < t.rows.length) t.rows.splice(i, 1);
    else if (o.op === "duplicate_row" && i < t.rows.length) t.rows.splice(i + 1, 0, [...t.rows[i]]);
    else if (o.op === "set_cell" && i < t.rows.length && names.includes(o.column)) t.rows[i][names.indexOf(o.column)] = o.value;
  }
  return t;
}
export const mutated = (tables: Table[], mutation: { table: string; ops: any[] }) => tables.map((t) => (t.name === mutation.table ? applyOps(t, mutation.ops) : t));
