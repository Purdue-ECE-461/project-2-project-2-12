import React, { useState, useEffect } from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

import axios from "axios";

function createData(packageName, packageURL, version) {
  return { packageName, packageURL, version };
}

function translateData(apiData) {
  const rows = [];
  for (const [key, value] of Object.entries(apiData)) {
    rows.push(createData(value["name"], value["url"], value["version"]));
  }

  console.log(rows);
  return rows;
}

let url = "https://ece-461-pyapi.ue.r.appspot.com/getPackageList";

export default function Header() {
  const [tableData, setTableData] = useState([]);
  let rows = translateData(tableData);

  // Component will mount
  useEffect(() => {
    (async () => {
      const result = await axios(url);
      console.log(result);
      setTableData(result.data["items"]);
    })();
  }, []);

  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        top: "50%",
        transform: "translate(-50%, -50%)",
      }}
    >
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Package Name</TableCell>
              <TableCell align="left">Package URL</TableCell>
              <TableCell align="right">Package Version</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => (
              <TableRow
                key={row.packageName}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {row.packageName}
                </TableCell>
                <TableCell align="left">{row.packageURL}</TableCell>
                <TableCell align="right">{row.version}</TableCell>
                <TableCell align="right">Upload</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
