<script lang="ts">
  import { getInitials } from "$lib/utils"
  import EmbeddedPage from "$lib/components/EmbeddedPage.svelte";

  type NodeType = 'Portfolio' | 'Program' | 'Project';
  type DataSet = 'Hierarchy' | 'Budget' | 'Organization' | 'Forecast' | 'Scope' | 'Risk' | 'Schedule' | 'Actuals' | 'Material' | 'Travel' | 'General' | 'SE' | 'HW' | 'SW';

  interface Repository {
    url: string;
    dataSets: DataSet[];
  }

  interface Node {
    id: string;
    name: string;
    type: NodeType;
    description: string;
    parentId: string | null;
    enabledFeatures: string[];
    repositories: Repository[];
  }

  let username = '';
  let password = '';
  let isLoggedIn = false;
  let activeTab = 'Home';
  let activeSidebarTab = 'Dashboard';
  let activePMTab = 'Dashboard';
  let isPinned = true;
  let forceShowToolbar = false;
  let showUserDropdown = false;
  let theme = 'dark';

  const ALL_DATA_SETS: DataSet[] = ['Hierarchy', 'Budget', 'Organization', 'Forecast', 'Scope', 'Risk', 'Schedule', 'Actuals', 'Material', 'Travel', 'General', 'SE', 'HW', 'SW'];

  // State for Hierarchy
  let nodes: Node[] = [
    {
      id: 'root',
      name: 'Global Portfolio',
      type: 'Portfolio',
      description: 'The top level portfolio for all operations.',
      parentId: null,
      enabledFeatures: ['PM', 'Plan', 'SE', 'UX', 'Dev', 'Doc', 'AI'],
      repositories: [
        { url: 'https://github.com/org/root-repo', dataSets: [...ALL_DATA_SETS] }
      ]

    }
  ];
  let activeNodeId = 'root';
  let navigationStack = ['root'];

  $: activeNode = nodes.find(n => n.id === activeNodeId) || nodes[0];
  $: currentNavNodeId = navigationStack[navigationStack.length - 1];
  $: currentNavNode = nodes.find(n => n.id === currentNavNodeId) || nodes[0];
  $: childNodes = nodes.filter(n => n.parentId === (currentNavNodeId ?? null));
  
  $: availableFeatures = ['Home', ...(activeNode?.enabledFeatures || [])];

  const allTabs = ["Home", "PM", "Plan", "SE", "UX", "Dev", "Doc", "AI"];
  
  const pmTabs = [
    { id: 'Dashboard', icon: '📊' },
    { id: 'Scope', icon: '🎯' },
    { id: 'Organization', icon: '👥' },
    { id: 'Budget', icon: '💰' },
    { id: 'Actuals', icon: '📈' },
    { id: 'Risk & Opportunity', icon: '⚠️' },
    { id: 'Forecast', icon: '🔮' },
    { id: 'Schedule', icon: '📅' },
    { id: 'Material', icon: '📦' },
    { id: 'Travel', icon: '✈️' }
  ];

  const tabUrls: Record<string, string> = {
    'Plan': 'https://svelte.dev',
    'SE': 'https://svelte.dev',
    'UX': 'https://penpot.app/',
    'Dev': 'https://svelte.dev'
  };

  // Node Management Functions
  function createNode(type: NodeType) {
    const name = prompt(`Enter name for new ${type}:`);
    if (!name) return;

    const newNode: Node = {
      id: Math.random().toString(36).substr(2, 9),
      name,
      type,
      description: '',
      parentId: currentNavNodeId || null,
      enabledFeatures: [],
      repositories: [
        { url: '', dataSets: [...ALL_DATA_SETS] }
      ]
    };

    nodes = [...nodes, newNode];
  }

  function deleteNode(id: string) {
    if (id === 'root') return;
    if (!confirm('Are you sure you want to delete this item and all its children?')) return;
    
    const getDescendants = (parentId: string): string[] => {
      const children = nodes.filter(n => n.parentId === parentId);
      return children.reduce((acc, child) => [...acc, child.id, ...getDescendants(child.id)], [] as string[]);
    };

    const toDelete = [id, ...getDescendants(id)];
    nodes = nodes.filter(n => !toDelete.includes(n.id));

    if (activeNodeId && toDelete.includes(activeNodeId)) {
      activeNodeId = 'root';
    }
    if (currentNavNodeId && toDelete.includes(currentNavNodeId)) {
      navigationStack = ['root'];
    }
  }

  function activateNode(id: string) {
    activeNodeId = id;
  }

  function navigateTo(id: string) {
    navigationStack = [...navigationStack, id];
  }

  function navigateBack() {
    if (navigationStack.length > 1) {
      navigationStack = navigationStack.slice(0, -1);
    }
  }

  function toggleFeature(nodeId: string, feature: string) {
    const node = nodes.find(n => n.id === nodeId);
    if (!node) return;
    
    const index = node.enabledFeatures.indexOf(feature);
    if (index === -1) {
      node.enabledFeatures = [...node.enabledFeatures, feature];
    } else {
      node.enabledFeatures = node.enabledFeatures.filter(f => f !== feature);
    }
    nodes = [...nodes];
  }

  function toggleDataSet(repoIndex: number, dataSet: DataSet) {
    if (!activeNode) return;
    const repo = activeNode.repositories[repoIndex];
    if (!repo) return;
    const index = repo.dataSets.indexOf(dataSet);
    if (index === -1) {
      repo.dataSets = [...repo.dataSets, dataSet];
    } else {
      repo.dataSets = repo.dataSets.filter(d => d !== dataSet);
    }
    nodes = [...nodes];
  }

  function addRepository() {
    if (!activeNode) return;
    activeNode.repositories = [...activeNode.repositories, { url: '', dataSets: [] }];
    nodes = [...nodes];
  }

  function removeRepository(index: number) {
    if (!activeNode) return;
    activeNode.repositories = activeNode.repositories.filter((_, i) => i !== index);
    nodes = [...nodes];
  }

  function updateRepoUrl(index: number, url: string) {
    if (!activeNode || !activeNode.repositories[index]) return;
    activeNode.repositories[index].url = url;
    nodes = [...nodes];
  }

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
    isPinned = true;
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
    padding: 0 1rem;
    position: relative;
    justify-content: center;
  }

  .active-node-name {
    position: absolute;
    left: 1rem;
    font-size: 0.9rem;
    font-weight: bold;
    color: #007bff;
    display: flex;
    align-items: center;
    height: 100%;
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

  .pin-btn, .theme-btn, .search-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.6;
    color: var(--item-text);
  }

  .pin-btn:hover, .theme-btn:hover, .search-btn:hover {
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
  }

  .content.shifted {
    margin-top: 60px;
    height: calc(100vh - 60px);
  }

  .sidebar {
    width: 60px;
    background: var(--toolbar-bg);
    border-right: 1px solid var(--toolbar-border);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1rem;
    gap: 1rem;
    z-index: 10;
    box-shadow: 2px 0 8px rgba(0,0,0,0.05);
  }

  .sidebar-item {
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 8px;
    cursor: pointer;
    color: var(--item-text);
    transition: all 0.2s;
    background: none;
    border: none;
  }

  .sidebar-item:hover {
    background: var(--item-hover);
    color: var(--text-color);
  }

  .sidebar-item.active {
    background: #007bff;
    color: white;
    box-shadow: 0 4px 12px rgba(0,123,255,0.3);
  }

  .main-view {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }

  .content-padded {
    padding: 2rem;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    box-sizing: border-box;
  }

  /* ShadCN/Material Mimicry */
  .card {
    background: var(--card-bg);
    border: 1px solid var(--toolbar-border);
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    padding: 1.5rem;
    transition: box-shadow 0.2s;
  }

  .card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }

  .dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
  }

  .stat-card {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .stat-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    color: var(--item-text);
    font-weight: 600;
    letter-spacing: 0.05em;
  }

  .stat-value {
    font-size: 1.5rem;
    font-weight: bold;
  }

  /* Hierarchy UI Styles */
  .hierarchy-nav {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
  }

  .nav-crumb {
    color: #007bff;
    cursor: pointer;
    background: none;
    border: none;
    padding: 0;
    font-size: inherit;
    font-family: inherit;
  }

  .nav-crumb:hover {
    text-decoration: underline;
  }

  .node-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }

  .node-card {
    padding: 1.5rem;
    background: var(--toolbar-bg);
    border: 1px solid var(--toolbar-border);
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    position: relative;
    transition: transform 0.2s;
  }

  .node-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }

  .node-card.active {
    border: 2px solid #007bff;
  }

  .node-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .node-type-badge {
    font-size: 0.7rem;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: 4px;
    background: #e9ecef;
    color: #495057;
  }

  .node-card.active .node-type-badge {
    background: #007bff;
    color: white;
  }

  .node-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: auto;
  }

  .btn-small {
    padding: 4px 8px;
    font-size: 0.75rem;
    border-radius: 4px;
    cursor: pointer;
    border: 1px solid var(--toolbar-border);
    background: var(--bg-color);
    color: var(--text-color);
  }

  .btn-small:hover {
    background: var(--item-hover);
  }

  .btn-activate {
    background: #28a745;
    color: white;
    border: none;
  }

  .btn-delete {
    background: #dc3545;
    color: white;
    border: none;
  }

  .feature-toggles {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--toolbar-border);
  }

  .feature-toggle {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 0.8rem;
    cursor: pointer;
  }

  .add-node-bar {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
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
      <div class="active-node-name">
        {activeNode?.name || 'No Selection'}
      </div>

      <div class="toolbar-center">
        {#each availableFeatures as tab}
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
          class="toolbar-item search-btn" 
          on:click={() => activeTab = 'Search'}
          title="Search"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </button>
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
      <aside class="sidebar">
        <button 
          class="sidebar-item" 
          class:active={activeSidebarTab === 'Dashboard'} 
          on:click={() => activeSidebarTab = 'Dashboard'}
          title="Dashboard"
        >
          <span style="font-size: 1.2rem;">📊</span>
        </button>
        <button 
          class="sidebar-item" 
          class:active={activeSidebarTab === 'Workspaces'} 
          on:click={() => activeSidebarTab = 'Workspaces'}
          title="Workspaces"
        >
          <span style="font-size: 1.2rem;">🏢</span>
        </button>
      </aside>

      <div class="main-view">
        {#if activeSidebarTab === 'Dashboard'}
          <div class="content-padded">
            <h1>Dashboard: {activeNode?.name || 'Selection'}</h1>
            <div class="dashboard-grid">
              <div class="card stat-card">
                <span class="stat-label">Type</span>
                <span class="stat-value">{activeNode?.type || 'N/A'}</span>
              </div>
              <div class="card stat-card">
                <span class="stat-label">Children</span>
                <span class="stat-value">{nodes.filter(n => n.parentId === activeNode?.id).length}</span>
              </div>
              <div class="card stat-card">
                <span class="stat-label">Enabled Features</span>
                <span class="stat-value">{activeNode?.enabledFeatures.length || 0}</span>
              </div>
            </div>
            
            <div class="card" style="margin-top: 2rem;">
              <h3>Description</h3>
              <p>{activeNode?.description || 'No description provided.'}</p>
            </div>

            <div class="card" style="margin-top: 1.5rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3>Git Repositories</h3>
                <button class="btn-small" on:click={addRepository}>+ Add Repo</button>
              </div>
              
              {#each activeNode?.repositories || [] as repo, i}
                <div style="margin-bottom: 1.5rem; padding: 1rem; border: 1px solid var(--toolbar-border); border-radius: 8px;">
                  <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <input 
                      type="text" 
                      placeholder="Repository URL" 
                      value={repo.url} 
                      on:input={(e) => updateRepoUrl(i, e.currentTarget.value)}
                      style="flex: 1; padding: 4px 8px; border-radius: 4px; border: 1px solid var(--toolbar-border); background: var(--bg-color); color: var(--text-color);"
                    />
                    <button class="btn-small btn-delete" on:click={() => removeRepository(i)}>Delete</button>
                  </div>
                  <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                    {#each ALL_DATA_SETS as ds}
                      <label style="font-size: 0.75rem; display: flex; align-items: center; gap: 4px;">
                        <input 
                          type="checkbox" 
                          checked={repo.dataSets.includes(ds)} 
                          on:change={() => toggleDataSet(i, ds)}
                        />
                        {ds}
                      </label>
                    {/each}
                  </div>
                </div>
              {/each}
              {#if (activeNode?.repositories || []).length === 0}
                <p style="color: var(--item-text); font-size: 0.9rem;">No repositories linked.</p>
              {/if}
            </div>
          </div>
        {:else if activeSidebarTab === 'Workspaces'}
          <div class="content-padded">
            <h1>Workspaces</h1>
            
            <div class="hierarchy-nav">
              <button class="nav-crumb" on:click={() => navigationStack = ['root']}>Global</button>
              {#each navigationStack.slice(1) as nodeId, i}
                <span>/</span>
                <button class="nav-crumb" on:click={() => navigationStack = navigationStack.slice(0, i + 2)}>
                  {nodes.find(n => n.id === nodeId)?.name}
                </button>
              {/each}
            </div>

            <div class="add-node-bar">
              {#if currentNavNode?.type === 'Portfolio'}
                <button class="btn-small" on:click={() => createNode('Portfolio')}>+ Portfolio</button>
                <button class="btn-small" on:click={() => createNode('Program')}>+ Program</button>
                <button class="btn-small" on:click={() => createNode('Project')}>+ Project</button>
              {:else if currentNavNode?.type === 'Program'}
                <button class="btn-small" on:click={() => createNode('Program')}>+ Program</button>
                <button class="btn-small" on:click={() => createNode('Project')}>+ Project</button>
              {:else if currentNavNode?.type === 'Project'}
                <button class="btn-small" on:click={() => createNode('Project')}>+ Project</button>
              {/if}
            </div>

            <div class="node-list">
              {#each childNodes as node}
                <div class="node-card card" class:active={node.id === activeNodeId}>
                  <div class="node-header">
                    <h3>{node.name}</h3>
                    <span class="node-type-badge">{node.type}</span>
                  </div>
                  <p>{node.description || 'No description provided.'}</p>
                  
                  <div class="feature-toggles">
                    {#each allTabs.slice(1) as feature}
                      <label class="feature-toggle">
                        <input 
                          type="checkbox" 
                          checked={node.enabledFeatures.includes(feature)} 
                          on:change={() => toggleFeature(node.id, feature)}
                        />
                        {feature}
                      </label>
                    {/each}
                  </div>

                  <div class="node-actions">
                    <button class="btn-small" on:click={() => navigateTo(node.id)}>Open</button>
                    <button class="btn-small btn-activate" on:click={() => activateNode(node.id)}>Activate</button>
                    <button class="btn-small btn-delete" on:click={() => deleteNode(node.id)}>Delete</button>
                  </div>
                </div>
              {/each}
            </div>
          </div>
        {/if}
      </div>
    {:else if activeTab === 'PM'}
      <aside class="sidebar">
        {#each pmTabs as pmTab}
          <button 
            class="sidebar-item" 
            class:active={activePMTab === pmTab.id} 
            on:click={() => activePMTab = pmTab.id}
            title={pmTab.id}
          >
            <span style="font-size: 1.2rem;">{pmTab.icon}</span>
          </button>
        {/each}
      </aside>
      <div class="main-view">
        <div class="content-padded">
          <h1>{activePMTab}: {activeNode?.name || 'Unknown'}</h1>
          <div class="card">
            <p>Stub content for {activePMTab} baseline management.</p>
          </div>
        </div>
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
        <h1>Documentation: {activeNode?.name || 'Unknown'}</h1>
        <p>Documentation for this {activeNode?.type || 'item'}.</p>
      </div>
    {:else if activeTab === 'AI'}
      <div class="content-padded">
        <h1>AI Assistant: {activeNode?.name || 'Unknown'}</h1>
        <p>AI capabilities tailored for {activeNode?.name || 'this item'}.</p>
      </div>
    {:else if activeTab === 'Profile'}
      <div class="content-padded">
        <h1>User Profile</h1>
        <p>User profile information.</p>
      </div>
    {:else if activeTab === 'Search'}
      <div class="content-padded">
        <h1>Search</h1>
        <div class="card">
          <input 
            type="text" 
            placeholder="Search workspaces, projects, or documents..." 
            style="width: 100%; padding: 0.75rem; border-radius: 8px; border: 1px solid var(--toolbar-border); background: var(--bg-color); color: var(--text-color);"
          />
          <div style="margin-top: 1.5rem; color: var(--item-text);">
            Enter a search term to find relevant content.
          </div>
        </div>
      </div>
    {/if}
  </main>
{/if}
</div>
