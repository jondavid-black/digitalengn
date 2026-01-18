<script lang="ts">
  import { getInitials } from "$lib/utils"
  import EmbeddedPage from "$lib/components/EmbeddedPage.svelte";

  let username = '';
  let password = '';
  let isLoggedIn = false;
  let activeTab = 'Home';
  let isPinned = false;
  let forceShowToolbar = false;
  let showUserDropdown = false;
  let theme = 'dark';

  const tabs = ["Home", "PM", "Plan", "SE", "UX", "Dev", "Doc", "AI"];
  
  const tabUrls: Record<string, string> = {
    'Plan': 'https://svelte.dev',
    'SE': 'https://svelte.dev',
    'UX': 'https://penpot.app/',
    'Dev': 'https://svelte.dev'
  };

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

  function handleLaunch(url: string, e: MouseEvent) {
    e.stopPropagation();
    window.open(url, '_blank');
  }

  function toggleTheme() {
    theme = theme === 'light' ? 'dark' : 'light';
  }

  $: if (typeof document !== 'undefined') {
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }
</script>

<style>
  :global(:root) {
    --bg-color: #ffffff;
    --text-color: #333333;
    --toolbar-bg: #ffffff;
    --toolbar-border: #eeeeee;
    --login-bg: #f5f5f5;
    --card-bg: #ffffff;
    --item-hover: #f0f0f0;
    --item-text: #666666;
  }

  :global(html.dark) {
    --bg-color: #1a1a1a;
    --text-color: #f0f0f0;
    --toolbar-bg: #2d2d2d;
    --toolbar-border: #404040;
    --login-bg: #121212;
    --card-bg: #2d2d2d;
    --item-hover: #3d3d3d;
    --item-text: #aaaaaa;
  }

  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    transition: background-color 0.3s, color 0.3s;
  }

  .app-container {
    min-height: 100vh;
    background-color: var(--bg-color);
    color: var(--text-color);
  }

  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: var(--login-bg);
  }

  .login-box {
    padding: 2rem;
    background: var(--card-bg);
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
    border: 1px solid var(--toolbar-border);
    border-radius: 4px;
    background: var(--bg-color);
    color: var(--text-color);
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
    background: var(--toolbar-bg);
    border-bottom: 1px solid var(--toolbar-border);
    z-index: 1000;
    transform: translateY(-90%);
    transition: transform 0.3s ease-in-out, background-color 0.3s, border-color 0.3s;
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
    background: transparent;
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
    color: var(--item-text);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 4px;
    transition: all 0.2s;
    background: none;
    border: none;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .launch-icon {
    opacity: 0.5;
    transition: opacity 0.2s;
    display: flex;
    align-items: center;
    background: none;
    border: none;
    padding: 2px;
    cursor: pointer;
    color: inherit;
  }

  .launch-icon:hover {
    opacity: 1;
    color: #007bff;
  }

  .toolbar-item:hover {
    background: var(--item-hover);
    color: var(--text-color);
  }

  .toolbar-item.active {
    color: #007bff;
    font-weight: bold;
  }

  .pin-btn, .theme-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.6;
    color: var(--item-text);
  }

  .pin-btn:hover, .theme-btn:hover {
    opacity: 1;
    color: var(--text-color);
    background: var(--item-hover);
  }

  .pin-btn.active {
    opacity: 1;
    color: #007bff;
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
    background: var(--toolbar-bg);
    border: 1px solid var(--toolbar-border);
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
    color: var(--text-color);
    text-align: left;
    background: none;
    border: none;
    cursor: pointer;
    transition: background 0.2s;
  }

  .dropdown-item:hover {
    background: var(--item-hover);
  }

  .content {
    margin-top: 20px;
    padding: 0;
    width: 100%;
    transition: margin-top 0.3s ease-in-out;
    height: calc(100vh - 20px);
    display: flex;
    flex-direction: column;
  }

  .content.shifted {
    margin-top: 60px;
    height: calc(100vh - 60px);
  }

  .content-padded {
    padding: 2rem;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    box-sizing: border-box;
  }
</style>

<div class="app-container">
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
            {#if tabUrls[tab]}
              {@const url = tabUrls[tab]}
              <button 
                class="launch-icon" 
                on:click={(e) => handleLaunch(url, e)}
                title="Open in new tab"
                aria-label={`Open ${tab} in new tab`}
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </button>
            {/if}
          </button>
        {/each}
      </div>

      <div class="toolbar-right">
        <button 
          class="toolbar-item theme-btn" 
          on:click={toggleTheme}
          title={theme === 'light' ? "Switch to Dark Mode" : "Switch to Light Mode"}
        >
          {#if theme === 'light'}
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
          {:else}
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
          {/if}
        </button>
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
      <div class="content-padded">
        <h1>Home Screen</h1>
        <p>Welcome to Digital Engine. This is the main dashboard.</p>
      </div>
    {:else if activeTab === 'PM'}
      <div class="content-padded">
        <h1>Project Management</h1>
        <p>Placeholder for PM capabilities.</p>
      </div>
    {:else if activeTab === 'Plan'}
      <EmbeddedPage src={tabUrls['Plan'] || ''} title="Planning" />
    {:else if activeTab === 'SE'}
      <EmbeddedPage src={tabUrls['SE'] || ''} title="Software Engineering" />
    {:else if activeTab === 'UX'}
      <EmbeddedPage src={tabUrls['UX'] || ''} title="User Experience" />
    {:else if activeTab === 'Dev'}
      <EmbeddedPage src={tabUrls['Dev'] || ''} title="Development" />
    {:else if activeTab === 'Doc'}
      <div class="content-padded">
        <h1>Documentation</h1>
        <p>Placeholder for Documentation capabilities.</p>
      </div>
    {:else if activeTab === 'AI'}
      <div class="content-padded">
        <h1>Artificial Intelligence</h1>
        <p>Placeholder for AI capabilities.</p>
      </div>
    {:else if activeTab === 'Profile'}
      <div class="content-padded">
        <h1>User Profile</h1>
        <p>Placeholder for User profile information.</p>
      </div>
    {/if}
  </main>
{/if}
</div>
