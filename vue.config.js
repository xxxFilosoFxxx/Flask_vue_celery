module.exports = {
  chainWebpack: (config) => {
    config
        .plugin('html')
        .tap((args) => {
          args[0].title = 'Tasks queue';
          return args;
        });
  },
  pluginOptions: {
    quasar: {
      importStrategy: 'kebab',
      rtlSupport: false
    }
  },
  transpileDependencies: [
    'quasar'
  ]
}
