<script lang="ts">
  import { signIn, signOut } from "@auth/sveltekit/client"
  import type { PageData } from "./$types"
  import { getInitials } from "$lib/utils"
  export let data: PageData
</script>

{#if data.session}
  <header style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: #f0f0f0;">
    <h1>Digital Engine</h1>
    <div style="display: flex; align-items: center; gap: 1rem;">
      <div style="text-align: right;">
        <div>{data.session.user?.name || 'User'}</div>
        <button on:click={() => signOut()} style="font-size: 0.8rem;">Logout</button>
      </div>
      <div style="width: 40px; height: 40px; border-radius: 50%; background: #ccc; display: flex; justify-content: center; align-items: center; font-weight: bold; cursor: pointer;" title="View Profile">
        {#if data.session.user?.image}
          <img src={data.session.user.image} alt="Avatar" style="width: 100%; height: 100%; border-radius: 50%;" />
        {:else}
          {getInitials(data.session.user?.name)}
        {/if}
      </div>
    </div>
  </header>

  <main style="padding: 2rem;">
    <h2>Welcome to your Dashboard</h2>
    <p>You are logged in as {data.session.user?.email}</p>
    <p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
  </main>
{:else}
  <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; gap: 2rem;">
    <h1>Digital Engine</h1>
    <p>Please log in to access the platform</p>
    <button on:click={() => signIn("keycloak")} style="padding: 1rem 2rem; font-size: 1.2rem; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 4px;">
      Login with Keycloak
    </button>
  </div>
{/if}
