import PropTypes from 'prop-types';
import { useState, useEffect, useMemo } from 'react';
import Typography from '@mui/material/Typography';
import serviceCaller from '../service';
import { TableHead, TableRow, TableCell, TableSortLabel, Box, Table, TableBody, Toolbar, Paper, TableContainer, TablePagination } from '@mui/material';
import { visuallyHidden } from '@mui/utils';
import { useNavigate } from 'react-router-dom';
import { Select, MenuItem } from '@mui/material';


function Models() {
    const [rows, setRows] = useState([]);
    const [namespaces, setNamespaces] = useState([]);


    useEffect(() => {
        serviceCaller.get({ route: '/db/models' })
            .then((res) => {
                setRows(res.data);
                setNamespaces(Array.from(new Set(res.data.map((row) => row.namespace))));
                }
            )
    }, []);

    const headCells = [
        {
          id: 'namespace',
          numeric: false,
          disablePadding: true,
          label: 'Namespace',
        },
        {
          id: 'model_name',
          numeric: true,
          disablePadding: false,
          label: 'Model Name',
        },
        {
          id: 'version',
          numeric: true,
          disablePadding: false,
          label: 'Version',
        },
        {
          id: 'state',
          numeric: true,
          disablePadding: false,
          label: 'state',
        },
        {
          id: 'tags',
          numeric: true,
          disablePadding: false,
          label: 'Tags',
        },
        {
          id: 'last_updated',
          numeric: true,
          disablePadding: false,
          label: 'Last Updated',
        },
      ];


    function descendingComparator(a, b, orderBy) {
        if (b[orderBy] < a[orderBy]) {
          return -1;
        }
        if (b[orderBy] > a[orderBy]) {
          return 1;
        }
        return 0;
    }

    function getComparator(order, orderBy) {
        return order === 'desc'
          ? (a, b) => descendingComparator(a, b, orderBy)
          : (a, b) => -descendingComparator(a, b, orderBy);
    }

    function EnhancedTableHead(props) {
        const { order, orderBy, onRequestSort } = props;
        const createSortHandler = (property) => (event) => {
            onRequestSort(event, property);
        };

        return (
          <TableHead>
            <TableRow>
              {headCells.map((headCell) => (
                <TableCell
                  key={headCell.id}
                  align={headCell.numeric ? 'right' : 'left'}
                  sortDirection={orderBy === headCell.id ? order : false}
                >
                  <TableSortLabel
                    active={orderBy === headCell.id}
                    direction={orderBy === headCell.id ? order : 'asc'}
                    onClick={createSortHandler(headCell.id)}
                  >
                    {headCell.label}
                    {orderBy === headCell.id ? (
                      <Box component="span" sx={visuallyHidden}>
                        {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                      </Box>
                    ) : null}
                  </TableSortLabel>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
        );
      }

    EnhancedTableHead.propTypes = {
        onRequestSort: PropTypes.func.isRequired,
        order: PropTypes.oneOf(['asc', 'desc']).isRequired,
        orderBy: PropTypes.string.isRequired,
        rowCount: PropTypes.number.isRequired,
    };

    function EnhancedTableToolbar(props) {

        return (
        <Toolbar
            sx={{
              pl: { sm: 2 },
              pr: { xs: 1, sm: 1 },
            }}
        >
            <Typography
                variant="h6"
                id="tableTitle"
                component="div"
            >
                Namespace:
            </Typography>
            <Select
                variant='standard'
                id="namespace-select-filter-standard"
                value={namespaces}
                label="namespace"
                defaultValue={namespaces[0]}
                // onChange={handleChange}
            >
                {namespaces.map((namespace, index) => (
                    <MenuItem key={index} value={namespace}>{namespace}</MenuItem>
                ))}
            </Select>
        </Toolbar>
        );
    }


    function EnhancedTable() {
        const navigate = useNavigate();
        const [order, setOrder] = useState('asc');
        const [orderBy, setOrderBy] = useState('calories');
        const [page, setPage] = useState(0);
        const [rowsPerPage, setRowsPerPage] = useState(25);

        function handleRequestSort(property) {
            const isAsc = orderBy === property && order === 'asc';
            setOrder(isAsc ? 'desc' : 'asc');
            setOrderBy(property);
        };

        function handleSelectModel(model_id) {
            navigate(`/model/${model_id}`)
        };

        function handleChangePage(event, newPage) {
            setPage(newPage);
        };

        function handleChangeRowsPerPage(event) {
            setRowsPerPage(parseInt(event.target.value, 10));
            setPage(0);
        };


        // Avoid a layout jump when reaching the last page with empty rows.
        const emptyRows =
          page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0;

        const visibleRows = useMemo(
          () =>
            rows.slice().sort(getComparator(order, orderBy)).slice(
              page * rowsPerPage,
              page * rowsPerPage + rowsPerPage,
            ),
          [order, orderBy, page, rowsPerPage],
        );


        return (
        <Box sx={{ width: '100%' }}>
            <Paper sx={{ width: '100%', mb: 2 }}>
                <EnhancedTableToolbar />
                <TableContainer>
                <Table
                    sx={{ minWidth: 750 }}
                    aria-labelledby="tableTitle"
                >
                <EnhancedTableHead
                    order={order}
                    orderBy={orderBy}
                    onRequestSort={handleRequestSort}
                    rowCount={rows.length}
                />
                <TableBody>
                    {visibleRows.map((row, index) => {
                    const labelId = `enhanced-table-checkbox-${index}`;

                    return (
                        <TableRow
                            hover
                            onClick={() => handleSelectModel(row.id)}
                            role="checkbox"
                            tabIndex={-1}
                            key={row.id}
                            sx={{ cursor: 'pointer' }}
                        >
                            <TableCell
                                component="th"
                                id={labelId}
                                scope="row"
                            >
                                {row.namespace}
                            </TableCell>
                            <TableCell align="right">{row.model_name}</TableCell>
                            <TableCell align="right">{row.model_version}</TableCell>
                            <TableCell align="right">{row.model_status}</TableCell>
                            <TableCell align="right">{row.tags}</TableCell>
                            <TableCell align="right">{row.last_updated}</TableCell>
                        </TableRow>
                    );
                    })}
                    {emptyRows > 0 && (
                        <TableRow>
                            <TableCell colSpan={6} />
                        </TableRow>
                    )}
                        </TableBody>
                    </Table>
                </TableContainer>
            <TablePagination
                rowsPerPageOptions={[25, 50, 100]}
                component="div"
                count={rows.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
            </Paper>
        </Box>
        );
    }
    return (
        <EnhancedTable />
    );
}

export default Models;
