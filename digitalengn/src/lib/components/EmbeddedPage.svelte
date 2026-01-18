<script lang="ts">
  export let src: string;
  export let title: string = "Embedded Content";
</script>

<style>
  .embedded-frame {
    width: 100%;
    height: 100%;
    border: none;
    background: white;
  }
</style>

<iframe {src} {title} class="embedded-frame"></iframe>
