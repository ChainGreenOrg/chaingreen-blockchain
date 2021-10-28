import React, { ReactNode } from 'react';
import { Trans, Plural } from '@lingui/macro';
import NumberFormat from 'react-number-format';
import {
  Box,
  InputAdornment,
  FormControl,
  FormHelperText,
} from '@material-ui/core';
import { useWatch, useFormContext } from 'react-hook-form';
import TextField, { TextFieldProps } from '../TextField';
import { chaingreen_to_mio } from '../../../../util/chaingreen';
import useCurrencyCode from '../../../../hooks/useCurrencyCode';
import FormatLargeNumber from '../FormatLargeNumber';
import Flex from '../Flex';

interface NumberFormatCustomProps {
  inputRef: (instance: NumberFormat | null) => void;
  onChange: (event: { target: { name: string; value: string } }) => void;
  name: string;
}

function NumberFormatCustom(props: NumberFormatCustomProps) {
  const { inputRef, onChange, ...other } = props;

  function handleChange(values: Object) {
    onChange(values.value);
  }

  return (
    <NumberFormat
      {...other}
      getInputRef={inputRef}
      onValueChange={handleChange}
      thousandSeparator
      allowNegative={false}
      isNumericString
    />
  );
}

export type AmountProps = TextFieldProps & {
  children?: (props: { mio: number; value: string | undefined }) => ReactNode;
  name?: string;
};

export default function Amount(props: AmountProps) {
  const { children, name, variant, fullWidth, ...rest } = props;
  const { control } = useFormContext();
  const currencyCode = useCurrencyCode();

  const value = useWatch<string>({
    control,
    name,
  });

  const mio = chaingreen_to_mio(value);

  return (
    <FormControl variant={variant} fullWidth={fullWidth}>
      <TextField
        name={name}
        variant={variant}
        autoComplete="off"
        InputProps={{
          spellCheck: false,
          inputComponent: NumberFormatCustom as any,
          endAdornment: (
            <InputAdornment position="end">{currencyCode}</InputAdornment>
          ),
        }}
        {...rest}
      />

        <FormHelperText component='div' >
          <Flex alignItems="center" gap={2}>
            <Flex flexGrow={1} gap={1}>
              {!!mio && (
                <>
                  <FormatLargeNumber value={mio} />
                  <Box>
                    <Plural value={mio} one="mio" other="mios" />
                  </Box>
                </>
              )}
            </Flex>
            {children &&
              children({
                mio,
                value,
              })}
          </Flex>
        </FormHelperText>
    </FormControl>
  );
}

Amount.defaultProps = {
  label: <Trans>Amount</Trans>,
  name: 'amount',
  children: undefined,
};
