import React from 'react';
import MuiButton, { ButtonProps as MuiButtonProps } from '@mui/material/Button';

export type ButtonProps = Omit<MuiButtonProps, 'variant' | 'color'> & { variant?: 'primary' | 'secondary' | 'default' };

const variantMap: Record<NonNullable<ButtonProps['variant']>, { muiVariant: MuiButtonProps['variant']; color: MuiButtonProps['color'] }> = {
  primary: { muiVariant: 'contained', color: 'primary' },
  secondary: { muiVariant: 'outlined', color: 'secondary' },
  default: { muiVariant: 'text', color: 'inherit' }
};

export const Button: React.FC<ButtonProps> = ({ children, variant = 'default', ...rest }) => {
  const { muiVariant, color } = variantMap[variant];
  return (
    <MuiButton variant={muiVariant} color={color} {...rest}>
      {children}
    </MuiButton>
  );
};

export default Button;
