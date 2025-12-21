import React from 'react';
import TextField from '@mui/material/TextField';

export type InputProps = React.ComponentProps<typeof TextField>;

export const Input: React.FC<InputProps> = (props) => {
  return <TextField fullWidth margin="normal" {...props} />;
};

export default Input;