import React, { useState, useEffect } from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

function createData(packageName, packageURL, rating) {
  return { packageName, packageURL, rating };
}

function translateData(apiData) {
  const rows = [];
  for (const [key, value] of Object.entries(apiData)) {
    rows.push(createData(value["name"], value["url"], value["rating"]));
  }

  console.log(rows);
  return rows;
}

const url = "http://127.0.0.1:5000/getPackages";

export default function Header() {
  const [tableData, setTableData] = useState([]);

  // Component will mount
  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then((res) => setTableData(res));
  }, []);

  const rows = translateData(tableData);

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
              <TableCell align="right">Overall Rating</TableCell>
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
                <TableCell align="right">{row.rating}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
