import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',

  fullyParallel: false,

  forbidOnly: !!process.env.CI,

  retries: 0,

  workers: 1,

  timeout: 30_000,

  expect: {
    timeout: 7_500,
  },

  reporter: [
    ['list'],
    [
      'html',
      {
        outputFolder: 'playwright-report',
        open: 'never',
      },
    ],
  ],

  use: {
    baseURL: 'http://127.0.0.1:8501',

    trace: 'retain-on-failure',

    screenshot: 'only-on-failure',

    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
  ],

  webServer: {
    command: 'C:\\Users\\gina.villanueva\\Proyectos\\App-Deteccion-Prod-M4\\.venv\\Scripts\\python.exe -m streamlit run demo\\app_operativa_v2.py --server.port 8501 --server.address 127.0.0.1 --server.headless true',

    url: 'http://127.0.0.1:8501',

    reuseExistingServer: true,

    timeout: 120_000,
  },
});
