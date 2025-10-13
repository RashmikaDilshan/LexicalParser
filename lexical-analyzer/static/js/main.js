// Main JavaScript for Lexical Analyzer & Parser

let currentResult = null;
let currentTreeFormat = 'visual';

// Set input value from test cases
function setInput(value) {
    document.getElementById('inputExpr').value = value;
}

// Analyze expression
async function analyzeExpression() {
    const input = document.getElementById('inputExpr').value.trim();
    
    if (!input) {
        alert('Please enter an expression to analyze');
        return;
    }
    
    // Show loading state
    const analyzeBtn = document.getElementById('analyzeBtn');
    const originalText = analyzeBtn.textContent;
    analyzeBtn.textContent = '⏳ Analyzing...';
    analyzeBtn.disabled = true;
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: input })
        });
        
        const result = await response.json();
        currentResult = result;
        
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while analyzing the expression');
    } finally {
        analyzeBtn.textContent = originalText;
        analyzeBtn.disabled = false;
    }
}

// Display analysis results
function displayResults(result) {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    
    // Display status
    displayStatus(result);
    
    // Display errors if any
    displayErrors(result);
    
    // Display tokens
    displayTokens(result);
    
    // Display parse tree
    displayParseTree(result);
    
    // Display statistics
    displayStatistics(result);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display status box
function displayStatus(result) {
    const statusBox = document.getElementById('statusBox');
    statusBox.className = 'status-box ' + (result.success ? 'success' : 'error');
    
    const icon = result.success ? '✅' : '❌';
    const text = result.success ? 'Input Accepted' : 'Input Rejected';
    
    statusBox.innerHTML = `
        <span style="font-size: 1.5em;">${icon}</span>
        <span>${text}</span>
    `;
}

// Display errors
function displayErrors(result) {
    const errorsBox = document.getElementById('errorsBox');
    
    if (result.errors && result.errors.length > 0) {
        errorsBox.style.display = 'block';
        
        let html = '<h3>⚠️ Errors Detected</h3>';
        result.errors.forEach((error, index) => {
            const location = error.line ? ` (Line ${error.line}${error.column ? ', Col ' + error.column : ''})` : '';
            html += `
                <div class="error-item">
                    <strong>${error.type}${location}:</strong><br>
                    ${error.message}
                    ${error.suggestion ? '<br><em>Suggestion: ' + error.suggestion + '</em>' : ''}
                </div>
            `;
        });
        
        errorsBox.innerHTML = html;
    } else {
        errorsBox.style.display = 'none';
    }
}

// Display tokens table
function displayTokens(result) {
    const tokensTable = document.getElementById('tokensTable');
    
    if (!result.tokens || result.tokens.length === 0) {
        tokensTable.innerHTML = '<p>No tokens generated</p>';
        return;
    }
    
    let html = `
        <table class="tokens-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Lexeme</th>
                    <th>Token Type</th>
                    <th>Category</th>
                    <th>Position</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    result.tokens.forEach((token, index) => {
        const categoryClass = getCategoryClass(token.category);
        html += `
            <tr>
                <td>${index + 1}</td>
                <td><code>${escapeHtml(token.lexeme)}</code></td>
                <td><span class="token-badge ${categoryClass}">${token.type}</span></td>
                <td>${token.category}</td>
                <td>Line ${token.line}, Col ${token.column}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    tokensTable.innerHTML = html;
}

// Get CSS class for token category
function getCategoryClass(category) {
    const classMap = {
        'Operator': 'token-operator',
        'Delimiter': 'token-delimiter',
        'Identifier': 'token-identifier',
        'Literal': 'token-literal'
    };
    return classMap[category] || '';
}

// Display parse tree
function displayParseTree(result) {
    if (!result.parse_tree) {
        document.getElementById('treeDisplay').innerHTML = '<p>No parse tree available</p>';
        return;
    }
    
    showTreeFormat(currentTreeFormat);
}

// Show tree in different formats
function showTreeFormat(format) {
    currentTreeFormat = format;
    
    if (!currentResult || !currentResult.parse_tree) {
        return;
    }
    
    const treeDisplay = document.getElementById('treeDisplay');
    
    if (format === 'visual') {
        treeDisplay.innerHTML = renderTreeVisual(currentResult.parse_tree);
    } else if (format === 'ascii') {
        treeDisplay.innerHTML = `<pre>${currentResult.tree_ascii || renderTreeAscii(currentResult.parse_tree)}</pre>`;
    } else if (format === 'svg') {
        treeDisplay.innerHTML = currentResult.tree_svg || '<p>SVG not available</p>';
    }
}

// Render tree visual format
function renderTreeVisual(node, level = 0) {
    if (!node) return '';
    
    const margin = level * 30;
    const nodeClass = getNodeClass(node.name);
    
    let html = `
        <div class="tree-node" style="margin-left: ${margin}px;">
            <span class="${nodeClass}">${escapeHtml(node.name)}</span>
    `;
    
    if (node.children && node.children.length > 0) {
        for (const child of node.children) {
            html += renderTreeVisual(child, level + 1);
        }
    }
    
    html += '</div>';
    return html;
}

// Render tree ASCII format
function renderTreeAscii(node, prefix = '', isLast = true) {
    if (!node) return '';
    
    let result = '';
    const connector = isLast ? '└── ' : '├── ';
    result += prefix + connector + node.name + '\n';
    
    if (node.children && node.children.length > 0) {
        const extension = isLast ? '    ' : '│   ';
        node.children.forEach((child, index) => {
            const childIsLast = index === node.children.length - 1;
            result += renderTreeAscii(child, prefix + extension, childIsLast);
        });
    }
    
    return result;
}

// Get node CSS class
function getNodeClass(name) {
    if (name === 'ε') return 'epsilon-node';
    if (name.startsWith('id') || name.startsWith('num')) return 'terminal-node';
    if (['+', '-', '*', '/', '%', '**'].includes(name)) return 'operator-node';
    if (['(', ')'].includes(name)) return 'delimiter-node';
    return 'non-terminal-node';
}

// Display statistics
function displayStatistics(result) {
    const statsDisplay = document.getElementById('statsDisplay');
    
    if (!result.statistics || Object.keys(result.statistics).length === 0) {
        statsDisplay.innerHTML = '<p>No statistics available</p>';
        return;
    }
    
    const stats = result.statistics;
    
    let html = '<div class="stats-grid">';
    
    const statsList = [
        { label: 'Total Nodes', value: stats.total_nodes },
        { label: 'Tree Height', value: stats.height },
        { label: 'Leaf Nodes', value: stats.leaf_count },
        { label: 'Non-Terminals', value: stats.non_terminals },
        { label: 'Terminals', value: stats.terminals },
        { label: 'Epsilon (ε)', value: stats.epsilon_count }
    ];
    
    statsList.forEach(stat => {
        if (stat.value !== undefined) {
            html += `
                <div class="stat-item">
                    <div class="stat-value">${stat.value}</div>
                    <div class="stat-label">${stat.label}</div>
                </div>
            `;
        }
    });
    
    html += '</div>';
    statsDisplay.innerHTML = html;
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Handle Enter key in input
document.addEventListener('DOMContentLoaded', function() {
    const inputExpr = document.getElementById('inputExpr');
    if (inputExpr) {
        inputExpr.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                analyzeExpression();
            }
        });
    }
});