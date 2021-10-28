import React from 'react';
import styled from 'styled-components';
import { Box, BoxProps } from '@material-ui/core';
import { Chaingreen } from '@chia/icons';

const StyledChaingreen = styled(Chaingreen)`
  max-width: 100%;
  width: auto;
  height: auto;
`;

export default function Logo(props: BoxProps) {
  return (
    <Box {...props}>
      <StyledChaingreen />
    </Box>
  );
}
