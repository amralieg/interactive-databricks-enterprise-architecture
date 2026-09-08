/*
  Industry icon map — the single source of truth for the emoji glyph that stands
  for each industry. Used by the browser (industry menu, page/tab title) and by the
  Node build tools (share stubs + per-industry cover images), so it is a UMD module
  like arch_schema.js. Emoji are chosen to be recognisable at a glance and render
  from the system emoji font everywhere (menu, browser tab, and the 1200x630 cover).
  Keep one entry per architectures/<id>.yaml; the generic/reference board uses ◈.
*/
(function (root, factory) {
  const M = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = M;
  else root.IndustryIcons = M;
})(typeof self !== "undefined" ? self : this, function () {
  const ICON = {
    advertising: "📣", aerospace_space: "🚀", agriculture: "🌾", agtech: "🌱",
    airlines: "✈️", apparel_fashion: "👗", automotive: "🚗", banking: "🏦",
    capital_markets: "📈", chemical_mfg: "⚗️", clinical_trials: "🧪", construction: "🏗️",
    consumer_goods: "🧴", crypto_digital_assets: "🪙", cybersecurity: "🛡️", data_centers: "🖥️",
    diagnostics_labs: "🔬", digital_health: "🩺", ecommerce: "🛍️", edtech: "🎓",
    education: "📚", energy_utilities: "⚡", food_beverage: "🍔", gaming: "🎮",
    genomics_biotech: "🧬", grocery: "🛒", health_insurance: "🏥", healthcare: "⚕️",
    insurance_pandc: "☂️", legal: "⚖️", life_insurance: "🕊️", manufacturing: "🏭",
    market_data_exchanges: "💹", media_broadcasting: "📺", medical_devices: "🩻", mining: "⛏️",
    mortgage_lending: "🏠", ngo: "🤝", oil_gas: "🛢️", paper_packaging: "🗞️",
    payments_fintech: "💳", pharmaceuticals: "💊", pharmacy_pbm: "🏪", professional_services: "💼",
    public_safety: "🚨", public_sector: "🏛️", rail_transit: "🚆", real_estate: "🏢",
    renewables: "🌿", restaurants: "🍽️", retail: "🏬", semiconductors: "💠",
    shipping_ports: "⚓", software_technology: "💻", sports_entertainment: "🏟️", staffing_hr: "👥",
    telecommunication: "📡", transport_shipping: "🚚", travel_hospitality: "🧳", waste_management: "🗑️",
    water_utilities: "💧", wealth_management: "💰", wholesale_distribution: "📦"
  };
  const GENERIC = "◈";
  function iconFor(id) {
    if (!id || id === "generic") return GENERIC;
    return ICON[id] || GENERIC;
  }
  return { ICON: ICON, GENERIC: GENERIC, iconFor: iconFor };
});
