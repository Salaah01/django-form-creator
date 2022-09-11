/**
 * Module overrides CRA app settings. The following overrides are applied:
 * - Change the output path to the static folder.
 * - Disable file hashing.
 */

const rewire = require("rewire");
const path = require("node:path");

const buildDefaults = rewire("react-scripts/scripts/build.js");
const pathsDefault = rewire("react-scripts/config/paths.js");

let config = buildDefaults.__get__("config");

const buildPath = path.resolve(
  __dirname,
  "..",
  "..",
  "..",
  path.join("static_2", "form_creator", "js", "form_setup")
);
console.log("writing files to ", buildPath);
pathsDefault.__set__("buildPath", buildPath);
pathsDefault.appBuild = buildPath;
buildDefaults.__set__("paths", pathsDefault);
config.output.path = buildPath;

// We won't hash the file names, this can be handled by Django instead of
// the user choices to do so.
config.output.filename = "static/js/[name].js";
config.output.chunkFilename = "static/js/[name].chunk.js";

config.plugins[5].options.filename = "static/css/[name].css";
config.plugins[5].options.moduleFilename = () => "static/css/main.css";
