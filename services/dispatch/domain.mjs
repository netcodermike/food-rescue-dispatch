export async function operation({ portions, cold, radiusKm, partners }, eligibility) {
  if (!Number.isSafeInteger(portions) || portions < 1) throw new TypeError('Expected positive integer portions')
  const { sites } = await eligibility({ cold, radiusKm, partners })
  const assignments = []
  let unassigned = portions
  for (const site of sites) {
    const count = Math.min(site.capacity, unassigned)
    if (count) assignments.push({ site: site.id, portions: count })
    unassigned -= count
    if (!unassigned) break
  }
  return { assignments, unassigned }
}
