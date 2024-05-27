const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm-bundler.js'
      }
    }
  }
})
module.exports = defineConfig({
  transpileDependencies: true,

  pluginOptions: {
    vuetify: {
		}
  }
})
module.exports = {
  outputDir: '../static',
  indexPath: '../test_datatable/templates/test_datatable/index.html',

  pluginOptions: {
    vuetify: {}
  },
};
