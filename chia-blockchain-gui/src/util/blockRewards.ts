import Big from 'big.js';

const MIO_PER_CHAINGREEN = Big(1000000000000);
const BLOCKS_PER_YEAR = 1681920;

export function calculatePoolReward(height: number): Big {
  if (height === 0) {
    return MIO_PER_CHAINGREEN.times(21000000).times(7 / 8);
  }
  if (height < 3 * BLOCKS_PER_YEAR) {
    return MIO_PER_CHAINGREEN.times(2).times(7 / 8);
  }
  if (height < 6 * BLOCKS_PER_YEAR) {
    return MIO_PER_CHAINGREEN.times(1).times(7 / 8);
  }
  if (height < 9 * BLOCKS_PER_YEAR) {
    return MIO_PER_CHAINGREEN.times(0.5).times(7 / 8);
  }
  if (height < 12 * BLOCKS_PER_YEAR) {
    return MIO_PER_CHAINGREEN.times(0.25).times(7 / 8);
  }

  return MIO_PER_CHAINGREEN.times(0.125).times(7 / 8);
}

export function calculateBaseFarmerReward(height: number): Big {
  if (height === 0) {
    return MIO_PER_CHAINGREEN.times(21000000).times(1 / 8);
  }
  if (height < 3 * BLOCKS_PER_YEAR) {
    return MIO_PER_CHAINGREEN.times(2).times(1 / 8);
  }
  if (height < 6 * BLOCKS_PER_YEAR) {
    return MIO_PER_CHAINGREEN.times(1).times(1 / 8);
  }
  if (height < 9 * BLOCKS_PER_YEAR) {
    return MIO_PER_CHAINGREEN.times(0.5).times(1 / 8);
  }
  if (height < 12 * BLOCKS_PER_YEAR) {
    return MIO_PER_CHAINGREEN.times(0.25).times(1 / 8);
  }

  return MIO_PER_CHAINGREEN.times(0.125).times(1 / 8);
}
