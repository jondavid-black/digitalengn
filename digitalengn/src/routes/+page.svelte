<script lang="ts">
  let username = '';
  let password = '';
  let isLoggedIn = false;
  let activeTab = 'Home';
  let isPinned = false;
  let forceShowToolbar = false;
  let showUserDropdown = false;

  const tabs = ["Home", "PM", "Plan", "SE", "UX", "Dev", "Doc"];

  function handleLogin() {
    if (username === 'admin' && password === 'admin') {
      isLoggedIn = true;
      forceShowToolbar = true;
      setTimeout(() => {
        forceShowToolbar = false;
      }, 3000);
    } else {
      alert('Invalid credentials');
    }
  }

  function handleLogout() {
    isLoggedIn = false;
    username = '';
    password = '';
    activeTab = 'Home';
    isPinned = false;
    forceShowToolbar = false;
    showUserDropdown = false;
  }

  function handleProfile() {
    activeTab = 'Profile';
    showUserDropdown = false;
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

  .toolbar:hover, .toolbar-trigger:hover + .toolbar, .toolbar.force-show, .toolbar.pinned {
    transform: translateY(0);
  }

  .toolbar.pinned {
    border-bottom: 2px solid #007bff;
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
    width: 100%;
    max-width: 1200px;
    padding: 0 1rem;
    position: relative;
    justify-content: center;
  }

  .toolbar-center {
    display: flex;
    gap: 1.5rem;
    align-items: center;
  }

  .toolbar-right {
    position: absolute;
    right: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
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

  .pin-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.6;
  }

  .pin-btn:hover {
    opacity: 1;
  }

  .pin-btn.active {
    opacity: 1;
  }

  .avatar-container {
    position: relative;
    display: flex;
    align-items: center;
  }

  .avatar-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #007bff;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 0.75rem;
    font-weight: bold;
    cursor: pointer;
    border: none;
    padding: 0;
  }

  .user-dropdown {
    position: absolute;
    top: 35px;
    right: 0;
    background: white;
    border: 1px solid #eee;
    border-radius: 4px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    min-width: 120px;
    z-index: 1002;
  }

  .dropdown-item {
    padding: 8px 12px;
    font-size: 0.85rem;
    color: #333;
    text-align: left;
    background: none;
    border: none;
    cursor: pointer;
    transition: background 0.2s;
  }

  .dropdown-item:hover {
    background: #f5f5f5;
  }

  .content {
    margin-top: 20px;
    padding: 2rem;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    transition: margin-top 0.3s ease-in-out;
  }

  .content.shifted {
    margin-top: 60px;
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
  <nav class="toolbar" class:force-show={forceShowToolbar} class:pinned={isPinned}>
    <div class="toolbar-inner">
      <div class="toolbar-center">
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

      <div class="toolbar-right">
        <button 
          class="toolbar-item pin-btn" 
          class:active={isPinned}
          on:click={() => isPinned = !isPinned}
          title={isPinned ? "Unpin Toolbar" : "Pin Toolbar"}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill={isPinned ? "currentColor" : "none"} stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="17" x2="12" y2="22"></line><path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.79-.9A2 2 0 0 1 15 10.76V6a3 3 0 0 0-3-3 3 3 0 0 0-3 3v4.76a2 2 0 0 1-1.1 1.79l-1.79.9A2 2 0 0 0 5 15.24Z"></path></svg>
        </button>
        <div class="avatar-container">
          <button class="avatar-circle" on:click={() => showUserDropdown = !showUserDropdown}>
            AD
          </button>
          {#if showUserDropdown}
            <div class="user-dropdown">
              <button class="dropdown-item" on:click={handleProfile}>Profile</button>
              <button class="dropdown-item" on:click={handleLogout}>Logout</button>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </nav>

  <main class="content" class:shifted={isPinned}>
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
    {:else if activeTab === 'Profile'}
      <h1>User Profile</h1>
      <p>Placeholder for User profile information.</p>
    {/if}
  </main>
{/if}
