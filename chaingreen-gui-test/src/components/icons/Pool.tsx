import React from 'react';
import { SvgIcon, SvgIconProps } from '@material-ui/core';
import { ReactComponent as PoolIcon } from './images/pool.svg';

export default function Pool(props: SvgIconProps) {
  return <SvgIcon component={PoolIcon} viewBox="0 0 34 34" {...props} />;
}
