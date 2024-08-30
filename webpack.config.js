const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require('terser-webpack-plugin');

const config = {
    entry: {
        index: [
            // path.join(__dirname, '/jtflask/static/src/index.css'),
            path.join(__dirname, '/jtflask/static/src/index.js')  // webpack: only the last one of the array can be exposed
        ]
    },
    // devtool: 'cheap-module-source-map',
    output: {
        path: path.join(__dirname, 'jtflask/static/assets/js/dist'),
        chunkFilename: 'chunks/[id].js',
        filename: "vendors.min.js",
        publicPath: '',
        library: 'vendors',
        clean: true
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
                enforce: 'pre',
                use: ["source-map-loader"],
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader'
                ]
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "../../css/dist/vendors.min.css",
            chunkFilename: "[id].css"
        })
    ]
};
module.exports = config;