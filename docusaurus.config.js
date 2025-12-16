
const lightCodeTheme = require('prism-react-renderer').themes.vsLight;
const darkCodeTheme = require('prism-react-renderer').themes.vsDark;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics — Essentials',
  tagline: 'AI-Native Textbook for Physical AI and Robotics',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://ai-robotics-textbook.vercel.app',  // Vercel deployment URL
  // Set the /<baseUrl>/ pathname under which your site is served
  // For root deployment on Vercel, use '/'
  baseUrl: '/',  // Root base URL for Vercel

  // GitHub pages deployment config.
  // If you aren't using GitHub Pages, you don't need these.
  // organizationName: 'Myc786',  // Your GitHub username/organization
  // projectName: 'ai-robotics-textbook',  // Keep this as your repository name

  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'ignore',

  // Even if you don't use internationalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Change this to your repository URL to enable the "edit this page" links
          editUrl:
            'https://github.com/Myc786/ai-robotics-textbook/edit/main/',
        },
        blog: {  showReadingTime: true,
          // Change this to your repository URL to enable the "edit this page" links
          editUrl:
            'https://github.com/Myc786/ai-robotics-textbook/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  // Expose environment variables to client via customFields
  customFields: {
    NEXT_PUBLIC_RAG_BACKEND_URL: process.env.NEXT_PUBLIC_RAG_BACKEND_URL || 'http://localhost:8000',
  },


  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Social card image for sharing
      image: 'img/physical-ai-social-card.jpg',  // Update this with your actual social card
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            to: '/rag-chat',
            label: 'RAG Chatbot',
            position: 'left',
          },
          {
            href: 'https://github.com/Myc786/ai-robotics-textbook',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Textbook',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/facebook/docusaurus',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
