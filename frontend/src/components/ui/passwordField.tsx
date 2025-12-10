import React from 'react';
import TextField from '@mui/material/TextField';

export type PasswordFieldProps = React.ComponentProps<typeof TextField>;

export const PasswordField: React.FC<PasswordFieldProps> = (props) => {
  return <TextField type="password" fullWidth margin="normal" {...props} />;
};

export default PasswordField;
