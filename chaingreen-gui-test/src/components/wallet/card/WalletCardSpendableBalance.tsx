import React from 'react';
import { Trans } from '@lingui/macro';
import FarmCard from '../../farm/card/FarmCard';
import useWallet from '../../../hooks/useWallet';
import useCurrencyCode from '../../../hooks/useCurrencyCode';
import { mio_to_chaingreen_string } from '../../../util/chaingreen';

type Props = {
  wallet_id: number;
};

export default function WalletCardSpendableBalance(props: Props) {
  const { wallet_id } = props;

  const { wallet, loading } = useWallet(wallet_id);
  const currencyCode = useCurrencyCode();

  const value = wallet?.wallet_balance?.spendable_balance;

  return (
    <FarmCard
      loading={loading}
      valueColor="secondary"
      title={<Trans>Spendable Balance</Trans>}
      tooltip={
        <Trans>
          This is the amount of Chaingreen that you can currently use to make
          transactions. It does not include pending farming rewards, pending
          incoming transactions, and Chaingreen that you have just spent but is not
          yet in the blockchain.
        </Trans>
      }
      value={
        <>
          {mio_to_chaingreen_string(value)} {currencyCode}
        </>
      }
    />
  );
}
