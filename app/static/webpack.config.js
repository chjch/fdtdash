const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');

const config = {
    entry:  path.resolve(__dirname, 'index.jsx'),
    // devtool: 'cheap-module-source-map',
    output: {
        path: __dirname + '/assets/js',
        filename: 'vendors.min.js',
    },
    optimization: {
        minimize: true,
        minimizer: [
            new TerserPlugin({
                terserOptions: {
                    compress: {
                        drop_console: true
                    },
                    mangle: true,
                    output: {
                        comments: false
                    }
                },
            }),
        ],
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css', '.ts', '.tsx']
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx|ts|tsx)$/,
                // exclude: /node_modules\/(?!(@loaders.gl\/i3s))/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-typescript']
                    }
                }
            }
        ]
    }
};
module.exports = config;