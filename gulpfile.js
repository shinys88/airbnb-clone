



const gulp = require("gulp");

const css = () => {
    const postCSS = require("gulp-postcss");
    var sass = require("gulp-sass")(require("node-sass"));
    // const sass = require("gulp-sass");
    // sass.compiler = require("node-sass");
    const minify = require("gulp-csso");
    return gulp
    .src("assets/scss/styles.scss") //파일 불러오기
    .pipe(sass().on("error", sass.logError)) //scss를 css로 변환
    .pipe(postCSS([require("tailwindcss"), require("autoprefixer")])) //postCSS => 룰추가//  tailwind 룰을 css로 변경  (예) @tailwind base )
    .pipe(minify()) // 코드 압축
    .pipe(gulp.dest("static/css"));
};

exports.default = css;