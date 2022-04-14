import Typography from "@mui/material/Typography";

export default function Entry({ url, hit }) {
  return (
    <Typography>{url} = {hit}</Typography>
  );
}
