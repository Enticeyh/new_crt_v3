module.exports = {
    // vue3 打包以后路径处理
    publicPath: "./", // 可以设置成相对路径，这样所有的资源都会被链接为相对路径，打出来的包可以被部署在任意路径
    outputDir: "dist", //打包时生成的生产环境构建文件的目录
    assetsDir: 'static', // 放置生成的静态资源 (js、css、img、fonts)
    css: {
        loaderOptions: {
            postcss: {
                plugins: [
                    require("postcss-pxtorem")({
                        // 把px单位换算成rem单位
                        rootValue: 192, // 换算的基数(设计图750的根字体为75)
                        // selectorBlackList: ['weui', 'mu'], // 忽略转换正则匹配项
                        propList: ["*"],
                    }),
                ],
            },
        },
    },
}