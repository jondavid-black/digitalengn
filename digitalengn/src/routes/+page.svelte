<script lang="ts">
  let username = '';
  let password = '';
  let isLoggedIn = false;
  let activeTab = 'Home';

  const tabs = ["Home", "PM", "Plan", "SE", "UX", "Dev", "Doc", "User"];

  function handleLogin() {
    if (username === 'admin' && password === 'admin') {
      isLoggedIn = true;
    } else {
      alert('Invalid credentials');
    }
  }

  function handleLogout() {
    isLoggedIn = false;
    username = '';
    password = '';
    activeTab = 'Home';
  }
</script>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }

  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f5f5f5;
  }

  .login-box {
    padding: 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 300px;
  }

  .login-box h1 {
    margin: 0 0 1rem 0;
    text-align: center;
    font-size: 1.5rem;
  }

  .login-box input {
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  .login-box button {
    padding: 0.75rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }

  .login-box button:hover {
    background-color: #0056b3;
  }

  .toolbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: white;
    border-bottom: 1px solid #eee;
    z-index: 1000;
    transform: translateY(-90%);
    transition: transform 0.3s ease-in-out;
  }

  .toolbar:hover, .toolbar-trigger:hover + .toolbar {
    transform: translateY(0);
  }

  .toolbar-trigger {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 10px;
    z-index: 1001;
  }

  .toolbar-inner {
    display: flex;
    gap: 1.5rem;
  }

  .toolbar-item {
    font-size: 0.85rem;
    color: #666;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 4px;
    transition: all 0.2s;
    background: none;
    border: none;
  }

  .toolbar-item:hover {
    background: #f0f0f0;
    color: #333;
  }

  .toolbar-item.active {
    color: #007bff;
    font-weight: bold;
  }

  .content {
    margin-top: 20px;
    padding: 2rem;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
  }

  .logout-btn {
    position: fixed;
    top: 10px;
    right: 20px;
    font-size: 0.8rem;
    cursor: pointer;
    background: none;
    border: 1px solid #ccc;
    padding: 2px 8px;
    border-radius: 4px;
    color: #666;
    z-index: 1001;
  }
</style>

{#if !isLoggedIn}
  <div class="login-container">
    <div class="login-box">
      <h1>Digital Engine</h1>
      <input type="text" placeholder="Username" bind:value={username} />
      <input type="password" placeholder="Password" bind:value={password} on:keydown={(e) => e.key === 'Enter' && handleLogin()} />
      <button on:click={handleLogin}>Login</button>
    </div>
  </div>
{:else}
  <div class="toolbar-trigger"></div>
  <nav class="toolbar">
    <div class="toolbar-inner">
      {#each tabs as tab}
        <button 
          class="toolbar-item" 
          class:active={activeTab === tab}
          on:click={() => activeTab = tab}
        >
          {tab}
        </button>
      {/each}
    </div>
  </nav>

  <button class="logout-btn" on:click={handleLogout}>Logout</button>

  <main class="content">
    {#if activeTab === 'Home'}
      <h1>Home Screen</h1>
      <p>Welcome to Digital Engine. This is the main dashboard.</p>
    {:else if activeTab === 'PM'}
      <h1>Project Management</h1>
      <p>Placeholder for PM capabilities.</p>
    {:else if activeTab === 'Plan'}
      <h1>Planning</h1>
      <p>Placeholder for Planning capabilities.</p>
    {:else if activeTab === 'SE'}
      <h1>Software Engineering</h1>
      <p>Placeholder for SE capabilities.</p>
    {:else if activeTab === 'UX'}
      <h1>User Experience</h1>
      <p>Placeholder for UX capabilities.</p>
    {:else if activeTab === 'Dev'}
      <h1>Development</h1>
      <p>Placeholder for Development capabilities.</p>
    {:else if activeTab === 'Doc'}
      <h1>Documentation</h1>
      <p>Placeholder for Documentation capabilities.</p>
    {:else if activeTab === 'User'}
      <h1>User Settings</h1>
      <p>Placeholder for User settings and profile.</p>
    {/if}
  </main>
{/if}
