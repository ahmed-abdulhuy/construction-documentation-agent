import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    primary: { main: "#1976d2" },  // construction-friendly blue
    secondary: { main: "#ff9800" }, // orange accent
  },
  shape: { borderRadius: 8 },
});
