// CSS check - if this runs, CSS is loaded
(function checkCSS() {
    const cssStatus = document.getElementById('css-status');
    cssStatus.innerHTML = 'OK';
    cssStatus.className = 'status ok';
})();

// Function to test connection
window.testConnection = async function() {
    const btn = document.querySelector('.test-btn');
    btn.textContent = 'Testing...';
    btn.disabled = true;
    
    try {
        const response = await fetch('/api/env-info');
        const data = await response.json();
        
        // Update .env display
        const envDataPre = document.getElementById('env-data');
        envDataPre.textContent = JSON.stringify(data, null, 2);
        
        // Update .env status
        const envStatus = document.getElementById('env-status');
        if (data.STATUS === 'OK') {
            envStatus.innerHTML = 'OK';
            envStatus.className = 'status ok';
        } else {
            envStatus.innerHTML = 'ERROR';
            envStatus.className = 'status error';
        }
        
        alert('Connection successful! Check .env data below.');
    } catch (error) {
        console.error('Connection failed:', error);
        const envStatus = document.getElementById('env-status');
        envStatus.innerHTML = 'ERROR';
        envStatus.className = 'status error';
        alert('Connection failed! Make sure server is running.');
    } finally {
        btn.textContent = 'Test Connection';
        btn.disabled = false;
    }
};

// Update time
function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
    });
    document.getElementById('time').textContent = timeString;
}

// Load .env data on page load
async function loadEnvData() {
    try {
        const response = await fetch('/api/env-info');
        const data = await response.json();
        
        // Update .env display
        const envDataPre = document.getElementById('env-data');
        envDataPre.textContent = JSON.stringify(data, null, 2);
        
        // Update .env status
        const envStatus = document.getElementById('env-status');
        if (data.STATUS === 'OK') {
            envStatus.innerHTML = 'OK';
            envStatus.className = 'status ok';
        }
    } catch (error) {
        console.error('Failed to load .env data:', error);
        const envStatus = document.getElementById('env-status');
        envStatus.innerHTML = 'ERROR';
        envStatus.className = 'status error';
        document.getElementById('env-data').textContent = 'Failed to load .env data';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateTime();
    setInterval(updateTime, 1000);
    loadEnvData();
    
    // JS check
    const jsStatus = document.getElementById('js-status');
    jsStatus.innerHTML = 'OK';
    jsStatus.className = 'status ok';
});