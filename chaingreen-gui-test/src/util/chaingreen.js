const Big = require('big.js');
const units = require('./units');

// TODO: use bigint instead of float
const convert = (amount, from, to) => {
  if (Number.isNaN(Number.parseFloat(amount)) || !Number.isFinite(amount)) {
    return 0;
  }

  const amountInFromUnit = Big(amount).times(units.getUnit(from));

  return Number.parseFloat(amountInFromUnit.div(units.getUnit(to)));
};

class Chaingreen {
  constructor(value, unit) {
    this._value = value;
    this._unit = unit;
  }

  to(newUnit) {
    this._value = convert(this._value, this._unit, newUnit);
    this._unit = newUnit;

    return this;
  }

  value() {
    return this._value;
  }

  format() {
    const displayUnit = units.getDisplay(this._unit);

    const { format, fractionDigits, trailing } = displayUnit;

    let options = { maximumFractionDigits: fractionDigits };

    if (trailing) {
      options = { minimumFractionDigits: fractionDigits };
    }

    let value;

    if (fractionDigits !== undefined) {
      const fractionPower = Big(10).pow(fractionDigits);
      value = Number.parseFloat(
        Big(Math.floor(Big(this._value).times(fractionPower))).div(
          fractionPower,
        ),
      );
    } else {
      value = this._value;
    }

    let formatted = format.replace(
      '{amount}',
      Number.parseFloat(value).toLocaleString(undefined, options),
    );

    if (displayUnit.pluralize && this._value !== 1) {
      formatted += 's';
    }

    return formatted;
  }

  toString() {
    const displayUnit = units.getDisplay(this._unit);
    const { fractionDigits } = displayUnit;
    const options = { maximumFractionDigits: fractionDigits };
    return Number.parseFloat(this._value).toLocaleString(undefined, options);
  }
}

export const chaingreen_formatter = (value, unit) => new Chaingreen(value, unit);

chaingreen_formatter.convert = convert;
chaingreen_formatter.setDisplay = units.setDisplay;
chaingreen_formatter.setUnit = units.setUnit;
chaingreen_formatter.getUnit = units.getUnit;
chaingreen_formatter.setFiat = (currency, rate, display = null) => {
  units.setUnit(currency, 1 / rate, display);
};

export const mio_to_chaingreen = (mio) => {
  return chaingreen_formatter(Number.parseInt(mio), 'mio').to('chaingreen').value();
};

export const chaingreen_to_mio = (chaingreen) => {
  return chaingreen_formatter(Number.parseFloat(Number(chaingreen)), 'chaingreen')
    .to('mio')
    .value();
};

export const mio_to_chaingreen_string = (mio) => {
  return chaingreen_formatter(Number(mio), 'mio').to('chaingreen').toString();
};

export const mojo_to_colouredcoin = (mio) => {
  return chaingreen_formatter(Number.parseInt(mio), 'mio')
    .to('colouredcoin')
    .value();
};

export const colouredcoin_to_mojo = (colouredcoin) => {
  return chaingreen_formatter(Number.parseFloat(Number(colouredcoin)), 'colouredcoin')
    .to('mio')
    .value();
};

export const mojo_to_colouredcoin_string = (mojo) => {
  return chaingreen_formatter(Number(mojo), 'mio').to('colouredcoin').toString();
};
