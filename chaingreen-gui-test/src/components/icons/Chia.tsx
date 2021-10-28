import React from 'react';
import { SvgIcon, SvgIconProps } from '@material-ui/core';
import { ReactComponent as ChaingreenIcon } from './images/chaingreen.svg';

export default function Keys(props: SvgIconProps) {
  return <SvgIcon component={ChaingreenIcon} viewBox="0 0 800 600" {...props} />;
}
