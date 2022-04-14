import React from "react";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import CircularProgress from "@mui/material/CircularProgress";
import Button from "@mui/material/Button";
import Entry from "./Entry";

const API = "/";

class App extends React.Component {
  login = (username, password) => {
    this.setState({ loading: true });
    fetch(`${API}login`,
      {
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ username: username, password: password }),
        method: "POST",
      }).then(r => r.json()).then((j) => {
        if (j.logged_in === "fail") {
          alert("Cannot login");
        } else {
          this.setState({ whoami: "admin" });  
        }
    });
  };

  constructor(props) {
    super(props);
    this.stats = null;
    this.username = "";
    this.password = "";
    this.state = {
      loading: true,
      whoami: "",
      loginMethod: "",
    };
    fetch(`${API}whoami`).then(r => r.json()).then((j) => {
      this.setState({ whoami: j.youre });
      if (j.youre === "noone") {
        fetch(`${API}login`).then(r => r.json()).then((j) => {
          this.setState({ loginMethod: j.method });
          if (j.method === "open") {
            this.login("", "");
          } else {
            this.setState({ loginMethod: "auth" });
          }
        });
      }
    });
  }
  
  render() {
    const { whoami, loginMethod, loading } = this.state;

    if (whoami === "admin") {
      fetch(`${API}stats`).then((r) => r.json()).then((j) => {
          this.data = j;
          this.setState({ loading: false });
      });
    } else if (whoami === "noone") {
      return (
        <>
          <Typography variant="h4">Access restricted!</Typography>
          <TextField
            placeholder="Username"
            onChange={(e) => { this.username = e.target.value; }} 
          />
          <TextField
            placeholder="Password"
            onChange={(e) => { this.password = e.target.value; }}
          />
          <Button
            onClick={() => this.login(this.username, this.password)}
          >
            Login
          </Button>
        </>
      );
    }
    if (!loading) {
      return (
        <>
          {
            Object.entries(this.data).map((entry) => {
              return <Entry url={entry[0]} hit={entry[1]} />;
            })
          }
        </>
      );
    } else {
      return (
        <>
          <Dialog open>
            <DialogTitle>Please wait...</DialogTitle>
            <DialogContent>
              <CircularProgress />
            </DialogContent>
          </Dialog>
        </>
      );
    }
  }
}

export default App;
