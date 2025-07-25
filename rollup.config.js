import commonjs from '@rollup/plugin-commonjs'
import { nodeResolve } from '@rollup/plugin-node-resolve'
import terser from '@rollup/plugin-terser'

/**
 * Rollup config
 *
 * @type {RollupOptions}
 */
export default {
  input: 'lung_cancer_screening/assets/js/index.js',

  output: {
    compact: true,
    format: 'es',
    file: 'lung_cancer_screening/assets/compiled/js/bundle.js',

    plugins: [
      // Minification using terser
      terser({
        // Allow Terser to remove @preserve comments
        format: { comments: false },

        // Include sources content from source maps to inspect
        // NHS.UK frontend and other dependencies' source code
        sourceMap: {
          includeSources: true
        },

        // Compatibility workarounds
        safari10: true
      })
    ]
  },
  plugins: [
    // NHS.UK frontend uses commonjs, so we need to resolve and convert to ES modules
    nodeResolve({
      browser: true
    }),
    commonjs({
      requireReturnsDefault: 'preferred',
      defaultIsModuleExports: true
    }),
  ]
}

/**
 * @import { RollupOptions } from 'rollup'
 */
