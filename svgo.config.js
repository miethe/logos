module.exports = {
    plugins: [
      {
        name: 'preset-default',
        params: {
          // Keep ViewBox
          overrides: {
            removeViewBox: false
          },
        },
      },
      // Switch to ViewBox to fix scaling
      // Fixes 'Clipping' or tiny SVGs and broken CSS scaling
      'removeDimensions'
    ],
  };