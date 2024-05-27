export async function loadFonts () {
  const webFontLoader = await import('webfontloader')

  webFontLoader.load({
    custom: {
      families: ['Material Design Icons'],
      urls: ['http://127.0.0.1:8000/static/fonts/materialdesignicons-webfont.fbaef2a9.woff2']
    },
    google: {
      families: ['Roboto:100,300,400,500,700,900&display=swap'],
    },
  })
}