import React, { useState } from 'react';
import axios from 'axios';
import {
    Box,
    Button,
    Container,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography,
    Paper,
    CircularProgress,
    Alert,
} from '@mui/material';

const SparqlQuery = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const executeQuery = async () => {
        setLoading(true);
        setError('');
        setResults([]);
        try {
            const response = await axios.post('http://localhost:4000/sparql', { query });
            if (response.data.results.bindings.length === 0) {
                setError('No results found.');
            } else {
                setResults(response.data.results.bindings);
            }
        } catch (error) {
            setError('Error executing query. Please check your SPARQL syntax or server connection.');
            console.error('Error executing query:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="lg" sx={{ mt: 9, backgroundColor: '#f9f9f9', p: 7, borderRadius: 5 }}>
            <Typography variant="h4" gutterBottom textAlign="center" color="primary">
                SparqlQuery UI 
            </Typography>

            {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

            <Box component={Paper} sx={{ p: 3, mb: 3 }}>
                <TextField
                    fullWidth
                    multiline
                    rows={5}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Enter your SPARQL query"
                    variant="outlined"
                    label="SPARQL Query"
                />

                <Button
                    variant="contained"
                    color="primary"
                    onClick={executeQuery}
                    disabled={loading}
                    sx={{ mt: 2 }}
                >
                    {loading ? <CircularProgress size={24} sx={{ color: 'white' }} /> : 'Execute'}
                </Button>
            </Box>

            {results.length > 0 && (
                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                {Object.keys(results[0]).map((key) => (
                                    <TableCell key={key} sx={{ fontWeight: 'bold' }}>
                                        {key}
                                    </TableCell>
                                ))}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {results.map((result, index) => (
                                <TableRow key={index}>
                                    {Object.values(result).map((value, i) => (
                                        <TableCell key={i}>{value.value}</TableCell>
                                    ))}
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}
        </Container>
    );
};

export default SparqlQuery;
