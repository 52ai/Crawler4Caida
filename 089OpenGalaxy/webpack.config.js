const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyPlugin = require("copy-webpack-plugin");

let port = process.env.PORT || 8080;
let isProduction = process.env.IS_WEBPACK_PRODUCTION_MODE || false;

module.exports = {
  mode: isProduction ? "production" : "development",

  entry: ["react-hot-loader/patch", "./src/index.js"],

  devtool: isProduction ? false : "eval",

  devServer: {
    static: "./build",
    port: port,
    hot: true, // default true since webpack v4.0.0
  },

  plugins: [
    new HtmlWebpackPlugin({
      template: "./src/index.html",
    }),
    new MiniCssExtractPlugin({ filename: "styles.css" }),
    new CopyPlugin({
      patterns: [
        {
          from: __dirname + "/public",
          to: __dirname + "/build/public",
        },
      ],
    }),
  ],

  output: {
    path: path.resolve(__dirname, "build"),
    filename: "[name].js",
    publicPath: "",
    clean: true,
  },

  module: {
    rules: [
      {
        test: /\.jsx?$/,
        include: [path.resolve(__dirname, "src")],
        use: [
          {
            loader: "babel-loader", // babel-loader options are in .babelrc
          },
        ],
      },
      {
        test: /\.less$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "less-loader"],
      },
      {
        test: /\.(woff|woff2|eot|ttf|svg)$/,
        dependency: { not: ["url"] }, // Disable asset modules feature provided by webpack 5
        use: [
          {
            loader: "url-loader",
            options: {
              limit: 1,
              name: "[name].[ext]",
            },
          },
        ],
        type: "javascript/auto", // Disable asset modules feature provided by webpack 5
      },
      {
        test: /\.(png|jpg)$/,
        use: [
          {
            loader: "url-loader",
            options: {
              limit: 8192,
              name: "images/[name].[ext]",
            },
          },
        ],
      },
    ],
  },

  optimization: {
    splitChunks: {
      chunks: 'all',
      minSize: 20000,
      minRemainingSize: 0,
      minChunks: 1,
      maxAsyncRequests: 30,
      maxInitialRequests: 30,
      enforceSizeThreshold: 50000,
      cacheGroups: {
        defaultVendors: {
          test: /[\\/]node_modules[\\/]/,
          priority: -10,
          reuseExistingChunk: true,
        },
        default: {
          minChunks: 2,
          priority: -20,
          reuseExistingChunk: true,
        },
      },
    },
  },

  resolve: {
    extensions: ["*", ".js", ".jsx"],
    fallback: {
      fs: false,
      http: false,
      https: false,
      zlib: false,
      stream: false,
    },
  },

  node: {
    global: true,
  },
};
