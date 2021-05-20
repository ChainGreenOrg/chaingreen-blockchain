from chaingreen.util.ints import uint32, uint64

# 1 Chaingreen coin = 1,000,000,000,000 = 1 trillion mio.
_mio_per_chaingreen = 1000000000000
_blocks_per_year = 1681920  # 32 * 6 * 24 * 365


def calculate_pool_reward(height: uint32) -> uint64:
    """
    Returns the pool reward at a certain block height. The pool earns 7/8 of the reward in each block. If the farmer
    is solo farming, they act as the pool, and therefore earn the entire block reward.
    These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously.
    """
    if height == 0:
        return uint64(0)  # genesis block has no reward
    elif height < 4 * _blocks_per_year:
        return uint64(int((7 / 8) * 500 * _mio_per_chaingreen))
    elif height < 8 * _blocks_per_year:
        return uint64(int((7 / 8) * 250 * _mio_per_chaingreen))
    elif height < 12 * _blocks_per_year:
        return uint64(int((7 / 8) * 125 * _mio_per_chaingreen))
    elif height < 16 * _blocks_per_year:
        return uint64(int((7 / 8) * 72.5 * _mio_per_chaingreen))
    elif height < 20 * _blocks_per_year:
        return uint64(int((7 / 8) * 31.25 * _mio_per_chaingreen))
    elif height < 24 * _blocks_per_year:
        return uint64(int((7 / 8) * 15.625 * _mio_per_chaingreen))
    elif height < 28 * _blocks_per_year:
        return uint64(int((7 / 8) * 7.8125 * _mio_per_chaingreen))
    else:
        return uint64(0)


def calculate_base_farmer_reward(height: uint32) -> uint64:
    """
    Returns the base farmer reward at a certain block height.
    The base fee reward is 1/8 of total block reward

    Returns the coinbase reward at a certain block height. These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously.
    """
    if height < 4 * _blocks_per_year:
        return uint64(int((1 / 8) * 500 * _mio_per_chaingreen))
    elif height < 8 * _blocks_per_year:
        return uint64(int((1 / 8) * 250 * _mio_per_chaingreen))
    elif height < 12 * _blocks_per_year:
        return uint64(int((1 / 8) * 125 * _mio_per_chaingreen))
    elif height < 16 * _blocks_per_year:
        return uint64(int((1 / 8) * 72.5 * _mio_per_chaingreen))
    elif height < 20 * _blocks_per_year:
        return uint64(int((1 / 8) * 31.25 * _mio_per_chaingreen))
    elif height < 24 * _blocks_per_year:
        return uint64(int((1 / 8) * 15.625 * _mio_per_chaingreen))
    elif height < 28 * _blocks_per_year:
        return uint64(int((1 / 8) * 7.8125 * _mio_per_chaingreen))
    else:
        return uint64(0)
