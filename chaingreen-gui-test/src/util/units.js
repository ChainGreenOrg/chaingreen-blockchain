const units = {
  chaingreen: 1,
  mio: 1 / 1e12,
  colouredcoin: 1 / 1e9,
};

const aliases = {
  chaingreen: ['cgn', 'chaingreen', 'Chaingreen'],
  mio: ['mio', 'MIO'],
  colouredcoin: ['cc', 'colouredcoin'],
};

const display = {
  chaingreen: {
    format: '{amount} CGN',
    fractionDigits: 12,
  },
  mio: {
    format: '{amount} MIO',
    fractionDigits: 0,
  },
  colouredcoin: {
    format: '{amount} CC',
    fractionDigits: 3,
  },
};

const getUnitNameByAlias = (unitName) => {
  const name = unitName.toLowerCase();

  const alias = Object.keys(aliases).find((key) => aliases[key].includes(name));

  if (alias === undefined) {
    throw new Error(`Unit '${unitName}' is not supported`);
  }

  return alias;
};

const getUnitName = (unitName) => {
  const name = unitName.toLowerCase();

  const unit = units[name];

  if (unit !== undefined) return name;

  return getUnitNameByAlias(unitName);
};

const getUnit = (unit) => units[getUnitName(unit)];

const setDisplay = (unit, options) => {
  display[unit.toLowerCase()] = options;
};

const getDisplay = (unit) => display[getUnitName(unit)];

const setUnit = (unit, value, displayOptions = null) => {
  units[unit.toLowerCase()] = value;
  display[unit.toLowerCase()] =
    displayOptions !== null ? displayOptions : { format: `{amount} ${unit}` };
};

module.exports = {
  getUnit,
  setUnit,
  getDisplay,
  setDisplay,
};
