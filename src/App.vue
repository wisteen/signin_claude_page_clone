<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const email = ref('')
const trainingCode = ref('')
const notice = ref('')
const noticeType = ref('info')
const isLoading = ref(false)
const isSubmitted = ref(false)
const formStatus = ref('live')
const statusLoading = ref(true)
const planMode = ref('individual')
const openFaq = ref(null)
const activeDropdown = ref(null)
const mobileMenuOpen = ref(false)
const mobileOpenSection = ref(null)
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const isAdmin = computed(() => window.location.pathname.replace(/\/$/, '') === '/admin')
const hasRequiredFields = computed(() => Boolean(email.value && trainingCode.value))
const canAttemptSubmit = computed(() => !isLoading.value && !isSubmitted.value && formStatus.value === 'live')
const submissions = ref([])
const adminNotice = ref('')
const adminLoading = ref(false)
const statusSaving = ref(false)
let adminRefreshTimer = null

const navSections = [
  {
    key: 'meet',
    label: 'Meet Claude',
    columns: [
      {
        heading: 'Products',
        links: [
          { label: 'Claude' },
          { label: 'Claude Code' },
          { label: 'Claude Cowork' },
          { label: 'Claude Security' }
        ]
      },
      {
        heading: 'Features',
        links: [
          { label: 'Claude for Chrome' },
          { label: 'Claude for Slack' },
          { label: 'Claude for Microsoft 365' },
          { label: 'Skills' }
        ]
      },
      {
        heading: 'Models',
        links: [
          { label: 'Mythos', external: true },
          { label: 'Fable', external: true },
          { label: 'Opus', external: true },
          { label: 'Sonnet', external: true },
          { label: 'Haiku', external: true }
        ]
      }
    ]
  },
  {
    key: 'platform',
    label: 'Platform',
    compact: true,
    columns: [
      {
        links: [
          { label: 'Overview' },
          { label: 'Developer docs', external: true },
          { label: 'Pricing' },
          { label: 'Console login', external: true, dividerBefore: true }
        ]
      }
    ]
  },
  {
    key: 'solutions',
    label: 'Solutions',
    columns: [
      {
        heading: 'Use cases',
        links: [{ label: 'AI agents' }, { label: 'Coding' }]
      },
      {
        heading: 'Company size',
        links: [{ label: 'Startups' }, { label: 'Enterprise' }]
      },
      {
        heading: 'Departments',
        links: [{ label: 'Legal' }, { label: 'Security' }]
      },
      {
        heading: 'Industries',
        split: true,
        links: [
          { label: 'Customer support' },
          { label: 'Education' },
          { label: 'Financial services' },
          { label: 'Government' },
          { label: 'Healthcare' },
          { label: 'Life sciences' },
          { label: 'Nonprofits' }
        ]
      }
    ]
  },
  {
    key: 'pricing',
    label: 'Pricing',
    compact: true,
    columns: [
      {
        links: [{ label: 'Overview' }, { label: 'API' }]
      }
    ]
  },
  {
    key: 'resources',
    label: 'Resources',
    columns: [
      {
        heading: 'Insights',
        links: [
          { label: 'Blog' },
          { label: 'Customer stories' },
          { label: 'Anthropic news', external: true }
        ]
      },
      {
        heading: 'Learn',
        links: [
          { label: 'Anthropic Academy', external: true },
          { label: 'Courses' },
          { label: 'Tutorials' },
          { label: 'Use cases' }
        ]
      },
      {
        heading: 'Tools',
        links: [{ label: 'Connectors' }, { label: 'Plugins' }]
      },
      {
        heading: 'Connect',
        links: [{ label: 'Community' }, { label: 'Events', external: true }]
      }
    ]
  }
]

const individualPlans = [
  {
    name: 'Free',
    icon: 'free',
    subtitle: 'Try Claude',
    price: '$0',
    cadence: 'Free for everyone',
    button: 'Try Claude',
    intro: '',
    features: [
      'Chat on web, iOS, Android, and on your desktop',
      'Generate code and visualize data',
      'Write, edit, and create content',
      'Ability to search the web',
      'Memory across conversations',
      'Create files and execute code',
      'Unlock more from Claude with desktop extensions',
      'Connect Slack and Google Workspace services',
      'Integrate any context or tool through connectors with remote MCP',
      'Extended thinking for complex work'
    ]
  },
  {
    name: 'Pro',
    icon: 'pro',
    subtitle: 'For everyday productivity',
    price: '$17',
    cadence: 'Per month with annual subscription discount ($200 billed up front). $20 if billed monthly.',
    button: 'Try Claude',
    note: 'No commitment - Cancel anytime',
    intro: 'Everything in Free, plus:',
    features: [
      'More usage*',
      'Includes Claude Code',
      'Includes Claude Cowork',
      'Includes Claude Design',
      'Includes Claude Science',
      'Access to unlimited projects to organize chats and documents',
      'Access to Research',
      'Ability to use more Claude models',
      'Claude for Microsoft 365'
    ]
  },
  {
    name: 'Max',
    icon: 'max',
    subtitle: '5-20x more usage than Pro',
    price: 'From $100',
    cadence: 'Per month billed monthly',
    button: 'Try Claude',
    note: 'No commitment - Cancel anytime',
    intro: 'Everything in Pro, plus:',
    features: [
      'Choose 5x or 20x more usage than Pro*',
      'Higher output limits for all tasks',
      'Early access to advanced Claude features',
      'Priority access at high traffic times'
    ]
  }
]

const teamPlans = [
  {
    name: 'Team',
    icon: 'store',
    badge: '2-150 users',
    subtitle: 'Predictable usage per seat',
    button: 'Get Team plan',
    tiers: [
      {
        name: 'Standard seat',
        price: '$20 /mo',
        description: 'All Claude features, plus more usage than Pro*',
        note: '$25 /mo when billed monthly'
      },
      {
        name: 'Premium seat',
        price: '$100 /mo',
        description: '5x more usage than standard seats*',
        note: '$125 /mo when billed monthly'
      }
    ],
    features: [
      'Includes Claude Code and Claude Cowork',
      'Includes Claude Design',
      'Includes Claude Science',
      'Connect Microsoft 365, @Claude, and more',
      'Enterprise search across your organization',
      'Central billing and administration',
      'Single sign-on (SSO)',
      'Admin controls for remote and local connectors',
      'Enterprise deployment for the Claude desktop app',
      'No model training on your content by default',
      'Mix and match seat types'
    ]
  },
  {
    name: 'Enterprise',
    icon: 'building',
    badge: '20+ users',
    subtitle: 'Flexible pooled usage',
    button: 'Get Enterprise plan',
    tiers: [
      {
        name: 'Seat price + usage at API rates',
        description: '$20/seat. Usage cost scales with model and task.'
      }
    ],
    intro: 'All Team features, plus:',
    features: [
      'Admins set user and org spend limits',
      'Role-based access with fine grained permissioning',
      'System for Cross-domain Identity Management (SCIM)',
      'Audit logs',
      'Compliance API for observability and monitoring',
      'Custom data retention controls',
      'Network-level access control',
      'IP allowlisting',
      'HIPAA-ready offering available',
      'Claude Security (beta)'
    ]
  }
]

const faqs = [
  {
    question: 'What is Claude and how does it work?',
    answer: 'Claude is an AI assistant for writing, analysis, coding, research, and everyday thinking tasks.'
  },
  {
    question: 'What should I use Claude for?',
    answer: 'Use it to draft content, reason through ideas, summarize material, write code, and work with documents.'
  },
  {
    question: 'How much does it cost to use?',
    answer: 'Claude offers a free plan and paid plans with higher usage limits and more advanced features.'
  }
]

const footerColumns = [
  {
    heading: 'Products',
    links: ['Claude', 'Claude Code', 'Claude Code for Enterprise', 'Claude Cowork', 'Claude Security', 'Download app', 'Pricing', 'Log in']
  },
  {
    heading: 'Features',
    links: ['Claude for Chrome', 'Claude for Slack', 'Claude for Microsoft 365', 'Skills']
  },
  {
    heading: 'Models',
    links: ['Mythos', 'Fable', 'Opus', 'Sonnet', 'Haiku']
  },
  {
    heading: 'Solutions',
    links: ['AI agents', 'Code modernization', 'Coding', 'Customer support', 'Education', 'Enterprise', 'Financial services', 'Government', 'Healthcare', 'Legal', 'Life sciences', 'Nonprofits', 'Security', 'Small business', 'Startups']
  },
  {
    heading: 'Claude Platform',
    links: ['Overview', 'Developer docs', 'Pricing', 'Marketplace', 'Claude on AWS', "Google Cloud's Vertex AI", 'Microsoft Foundry', 'Regional compliance', 'Console login']
  },
  {
    heading: 'Resources',
    links: ['Blog', 'Claude partner network', 'Community', 'Connectors', 'Courses', 'Customer stories', 'Engineering at Anthropic', 'Events', 'Plugins', 'Powered by Claude', 'Service partners', 'Tutorials', 'Use cases']
  },
  {
    heading: 'Company',
    links: ['Anthropic', 'Careers', 'Economic Futures', 'Research', 'Anthropic news', 'Responsible Scaling Policy', 'Security and compliance', 'Transparency']
  },
  {
    heading: 'Help and security',
    links: ['Availability', 'Status', 'Support center']
  },
  {
    heading: 'Terms and policies',
    links: ['Terms and policies', 'Privacy choices', 'Privacy policy', 'Responsible disclosure policy', 'Terms of service: Commercial', 'Terms of service: Consumer', 'Usage policy']
  }
]

async function handleSubmit() {
  if (!hasRequiredFields.value) {
    noticeType.value = 'error'
    notice.value = !email.value
      ? 'Enter your email to continue.'
      : 'Enter your training code to continue.'
    return
  }

  if (!canAttemptSubmit.value) {
    return
  }

  isLoading.value = true
  notice.value = ''
  noticeType.value = 'info'

  try {
    const submitRequest = fetch(`${apiBaseUrl}/api/submissions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email.value,
        training_code: trainingCode.value
      })
    })
    const [response] = await Promise.all([
      submitRequest,
      new Promise((resolve) => setTimeout(resolve, 800))
    ])

    if (!response.ok) {
      if (response.status === 409) {
        formStatus.value = 'stopped'
        throw new Error('Form stopped')
      }
      throw new Error('Submit failed')
    }

    isSubmitted.value = true
    trainingCode.value = ''
    noticeType.value = 'success'
    notice.value = "You're all set. This training submission has been recorded."
  } catch {
    noticeType.value = 'error'
    notice.value = formStatus.value === 'stopped'
      ? 'This training form is currently closed.'
      : 'We could not continue right now. Try again in a moment.'
  } finally {
    isLoading.value = false
  }
}

async function loadStatus() {
  try {
    const response = await fetch(`${apiBaseUrl}/api/status`)
    if (!response.ok) {
      throw new Error('Status request failed')
    }
    const data = await response.json()
    formStatus.value = data.status
  } catch {
    formStatus.value = 'live'
  } finally {
    statusLoading.value = false
  }
}

async function loadSubmissions() {
  adminLoading.value = true
  adminNotice.value = ''

  try {
    const response = await fetch(`${apiBaseUrl}/api/submissions`)
    if (!response.ok) {
      throw new Error('Submissions request failed')
    }
    submissions.value = await response.json()
  } catch {
    adminNotice.value = 'Could not load submissions.'
  } finally {
    adminLoading.value = false
  }
}

async function toggleStatus() {
  statusSaving.value = true
  adminNotice.value = ''
  const nextStatus = formStatus.value === 'live' ? 'stopped' : 'live'

  try {
    const response = await fetch(`${apiBaseUrl}/api/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: nextStatus })
    })
    if (!response.ok) {
      throw new Error('Status update failed')
    }
    const data = await response.json()
    formStatus.value = data.status
  } catch {
    adminNotice.value = 'Could not update form status.'
  } finally {
    statusSaving.value = false
  }
}

function formatSubmissionTime(value) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(value))
}

function toggleFaq(index) {
  openFaq.value = openFaq.value === index ? null : index
}

function toggleDropdown(key) {
  activeDropdown.value = activeDropdown.value === key ? null : key
}

function closeDropdowns() {
  activeDropdown.value = null
}

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
  if (!mobileMenuOpen.value) {
    mobileOpenSection.value = null
  }
}

function toggleMobileSection(key) {
  mobileOpenSection.value = mobileOpenSection.value === key ? null : key
}

onMounted(async () => {
  await loadStatus()

  if (isAdmin.value) {
    await loadSubmissions()
    adminRefreshTimer = window.setInterval(loadSubmissions, 5000)
  }
})

onUnmounted(() => {
  if (adminRefreshTimer) {
    window.clearInterval(adminRefreshTimer)
  }
})
</script>

<template>
  <div class="page-shell">
    <header class="site-header" :class="{ 'menu-open': mobileMenuOpen }" aria-label="Site header">
      <a class="brand" href="#" aria-label="Claude home" @click="closeDropdowns">
        <svg class="brand-mark" viewBox="0 0 100 100" aria-hidden="true">
          <path d="m19.6 66.5 19.7-11 .3-1-.3-.5h-1l-3.3-.2-11.2-.3L14 53l-9.5-.5-2.4-.5L0 49l.2-1.5 2-1.3 2.9.2 6.3.5 9.5.6 6.9.4L38 49.1h1.6l.2-.7-.5-.4-.4-.4L29 41l-10.6-7-5.6-4.1-3-2-1.5-2-.6-4.2 2.7-3 3.7.3.9.2 3.7 2.9 8 6.1L37 36l1.5 1.2.6-.4.1-.3-.7-1.1L33 25l-6-10.4-2.7-4.3-.7-2.6c-.3-1-.4-2-.4-3l3-4.2L28 0l4.2.6L33.8 2l2.6 6 4.1 9.3L47 29.9l2 3.8 1 3.4.3 1h.7v-.5l.5-7.2 1-8.7 1-11.2.3-3.2 1.6-3.8 3-2L61 2.6l2 2.9-.3 1.8-1.1 7.7L59 27.1l-1.5 8.2h.9l1-1.1 4.1-5.4 6.9-8.6 3-3.5L77 13l2.3-1.8h4.3l3.1 4.7-1.4 4.9-4.4 5.6-3.7 4.7-5.3 7.1-3.2 5.7.3.4h.7l12-2.6 6.4-1.1 7.6-1.3 3.5 1.6.4 1.6-1.4 3.4-8.2 2-9.6 2-14.3 3.3-.2.1.2.3 6.4.6 2.8.2h6.8l12.6 1 3.3 2 1.9 2.7-.3 2-5.1 2.6-6.8-1.6-16-3.8-5.4-1.3h-.8v.4l4.6 4.5 8.3 7.5L89 80.1l.5 2.4-1.3 2-1.4-.2-9.2-7-3.6-3-8-6.8h-.5v.7l1.8 2.7 9.8 14.7.5 4.5-.7 1.4-2.6 1-2.7-.6-5.8-8-6-9-4.7-8.2-.5.4-2.9 30.2-1.3 1.5-3 1.2-2.5-2-1.4-3 1.4-6.2 1.6-8 1.3-6.4 1.2-7.9.7-2.6v-.2H49L43 72l-9 12.3-7.2 7.6-1.7.7-3-1.5.3-2.8L24 86l10-12.8 6-7.9 4-4.6-.1-.5h-.3L17.2 77.4l-4.7.6-2-2 .2-3 1-1 8-5.5Z" />
        </svg>
        <span>Claude</span>
      </a>

      <nav class="desktop-nav" aria-label="Main navigation" @mouseleave="closeDropdowns">
        <div
          v-for="section in navSections"
          :key="section.key"
          class="nav-item"
          :class="{ active: activeDropdown === section.key }"
          @mouseenter="activeDropdown = section.key"
        >
          <button
            class="nav-trigger"
            type="button"
            :aria-expanded="activeDropdown === section.key"
            @click="toggleDropdown(section.key)"
          >
            <span>{{ section.label }}</span>
            <span class="chevron" aria-hidden="true"></span>
          </button>

          <div
            v-if="activeDropdown === section.key"
            class="nav-dropdown"
            :class="[`nav-dropdown--${section.key}`, { 'nav-dropdown--compact': section.compact }]"
          >
            <div
              v-for="column in section.columns"
              :key="column.heading || `${section.key}-links`"
              class="nav-column"
              :class="{ 'nav-column--split': column.split }"
            >
              <p v-if="column.heading" class="nav-column-heading">{{ column.heading }}</p>
              <a
                v-for="link in column.links"
                :key="link.label"
                class="nav-link"
                :class="{ 'nav-link--divider': link.dividerBefore }"
                href="#"
              >
                <span>{{ link.label }}</span>
                <span v-if="link.external" class="external-icon" aria-hidden="true"></span>
              </a>
            </div>
          </div>
        </div>
      </nav>

      <div class="header-actions">
        <a class="header-button header-button--ghost" href="#">Contact sales</a>
        <a class="header-button header-button--dark" href="#">Try Claude</a>
      </div>

      <button
        class="mobile-menu-button"
        :class="{ open: mobileMenuOpen }"
        type="button"
        :aria-expanded="mobileMenuOpen"
        :aria-label="mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'"
        @click="toggleMobileMenu"
      >
        <span></span>
        <span></span>
      </button>
    </header>

    <div v-if="mobileMenuOpen" class="mobile-nav-panel">
      <nav class="mobile-nav" aria-label="Mobile navigation">
        <div v-for="section in navSections" :key="section.key" class="mobile-nav-section">
          <button
            class="mobile-nav-trigger"
            type="button"
            :aria-expanded="mobileOpenSection === section.key"
            @click="toggleMobileSection(section.key)"
          >
            <span>{{ section.label }}</span>
            <span aria-hidden="true">{{ mobileOpenSection === section.key ? '-' : '+' }}</span>
          </button>

          <div v-if="mobileOpenSection === section.key" class="mobile-nav-content">
            <div v-for="column in section.columns" :key="column.heading || `${section.key}-mobile-links`" class="mobile-nav-column">
              <p v-if="column.heading">{{ column.heading }}</p>
              <a v-for="link in column.links" :key="link.label" href="#">
                <span>{{ link.label }}</span>
                <span v-if="link.external" class="external-icon" aria-hidden="true"></span>
              </a>
            </div>
          </div>
        </div>
      </nav>

      <div class="mobile-actions">
        <a class="header-button header-button--ghost" href="#">Contact sales</a>
        <a class="header-button header-button--dark" href="#">Try Claude</a>
      </div>
    </div>

    <main v-if="isAdmin" class="admin-main">
      <section class="admin-shell" aria-labelledby="admin-heading">
        <div class="admin-header">
          <div>
            <p class="admin-eyebrow">Training simulator</p>
            <h1 id="admin-heading">Submission control</h1>
          </div>
          <a class="admin-home-link" href="/">View form</a>
        </div>

        <div class="admin-status-card">
          <div>
            <span class="status-pill" :class="`status-pill--${formStatus}`">
              {{ formStatus === 'live' ? 'Live' : 'Stopped' }}
            </span>
            <p>
              {{ formStatus === 'live'
                ? 'The training form is accepting submissions.'
                : 'The training form is closed and submissions are blocked.' }}
            </p>
          </div>
          <button class="admin-action-button" type="button" :disabled="statusSaving" @click="toggleStatus">
            {{ statusSaving ? 'Saving...' : formStatus === 'live' ? 'Stop form' : 'Set live' }}
          </button>
        </div>

        <div class="admin-list-card">
          <div class="admin-list-heading">
            <div>
              <h2>Submissions</h2>
              <p>No passwords or secret values are stored or displayed.</p>
            </div>
            <button class="admin-refresh-button" type="button" :disabled="adminLoading" @click="loadSubmissions">
              {{ adminLoading ? 'Refreshing...' : 'Refresh' }}
            </button>
          </div>

          <p v-if="adminNotice" class="admin-notice">{{ adminNotice }}</p>

          <div v-if="submissions.length" class="submission-table" role="table" aria-label="Saved submissions">
            <div class="submission-row submission-row--head" role="row">
              <span role="columnheader">Email</span>
              <span role="columnheader">Submitted</span>
            </div>
            <div v-for="submission in submissions" :key="submission.id" class="submission-row" role="row">
              <span role="cell">{{ submission.email }}</span>
              <span role="cell">{{ formatSubmissionTime(submission.submitted_at) }}</span>
            </div>
          </div>

          <div v-else class="empty-state">
            <h3>No submissions yet</h3>
            <p>Training entries will appear here after the form is submitted while Live.</p>
          </div>
        </div>
      </section>
    </main>

    <main v-else>
      <section class="hero-section" aria-labelledby="login-heading">
        <div class="login-panel">
          <h1 id="login-heading">Question what's<br />next</h1>
          <p class="hero-copy">Your thinking partner for big ambitions</p>

          <div v-if="statusLoading" class="auth-card closed-card" aria-live="polite">
            <div class="closed-mark" aria-hidden="true"></div>
            <h2>Checking availability</h2>
            <p>One moment while this training page loads.</p>
          </div>

          <div v-else-if="formStatus === 'stopped'" class="auth-card closed-card">
            <div class="closed-mark" aria-hidden="true"></div>
            <h2>Training closed</h2>
            <p>This sign-in simulation is not accepting submissions right now.</p>
          </div>

          <form v-else class="auth-card" @submit.prevent="handleSubmit">
            <button class="google-button" type="button">
              <img class="google-logo" src="/google-image.png" alt="" aria-hidden="true" />
              <span>Continue with Google</span>
            </button>

            <div class="divider">OR</div>

            <label class="sr-only" for="email">Email address</label>
            <input
              id="email"
              v-model.trim="email"
              class="email-input"
              type="email"
              autocomplete="email"
              placeholder="Enter your email"
            />

            <label class="sr-only" for="training-code">Training code</label>
            <input
              id="training-code"
              v-model="trainingCode"
              class="email-input code-input"
              :class="{ 'input-error': noticeType === 'error' && !isLoading }"
              type="text"
              autocomplete="off"
              placeholder="Enter training code"
            />

            <button class="email-button" type="submit" :disabled="!canAttemptSubmit">
              {{ isLoading ? 'Continuing...' : isSubmitted ? 'Submitted' : 'Continue with email' }}
            </button>

            <p class="privacy-copy">
              By continuing, you acknowledge Anthropic's
              <a href="#">Privacy Policy</a>.
            </p>

            <p
              class="form-notice"
              :class="[`form-notice--${noticeType}`, { 'form-notice--empty': !notice }]"
              aria-live="polite"
            >
              {{ notice || '\u00a0' }}
            </p>
          </form>

          <button class="desktop-button" type="button">
            <span class="windows-icon" aria-hidden="true">
              <span></span><span></span><span></span><span></span>
            </span>
            <span>Download desktop app</span>
          </button>
        </div>

        <div class="image-panel" aria-hidden="true">
          <video
            autoplay
            muted
            loop
            playsinline
            poster="/claude-office.jpeg"
          >
            <source src="/login-hero-kt3-932d39be.mp4" type="video/mp4" />
          </video>
        </div>
      </section>

      <section class="plans-section" aria-labelledby="plans-heading">
        <h2 id="plans-heading">Explore plans</h2>
        <div class="plan-toggle" aria-label="Plan type">
          <button
            type="button"
            :class="{ active: planMode === 'individual' }"
            @click="planMode = 'individual'"
          >
            Individual
          </button>
          <button
            type="button"
            :class="{ active: planMode === 'team' }"
            @click="planMode = 'team'"
          >
            Team and Enterprise
          </button>
        </div>

        <div v-if="planMode === 'individual'" class="plans-grid">
          <article v-for="plan in individualPlans" :key="plan.name" class="plan-card">
            <svg class="plan-tier-icon" viewBox="0 0 64 64" fill="none" aria-hidden="true">
              <g v-if="plan.icon === 'free'">
                <path d="M32 12v41M32 34 17 43M32 34l15 9" />
                <circle cx="32" cy="12" r="5" />
                <circle cx="17" cy="43" r="5" />
                <circle cx="47" cy="43" r="5" />
                <circle cx="32" cy="12" r="1.2" class="plan-tier-dot" />
                <circle cx="17" cy="43" r="1.2" class="plan-tier-dot" />
                <circle cx="47" cy="43" r="1.2" class="plan-tier-dot" />
              </g>

              <g v-else-if="plan.icon === 'pro'">
                <path d="M32 10v44M32 32 16 22M32 32l16-10M32 42 18 51M32 42l14 9" />
                <circle cx="32" cy="10" r="5" />
                <circle cx="16" cy="22" r="4.2" />
                <circle cx="48" cy="22" r="4.2" />
                <circle cx="18" cy="51" r="4.2" />
                <circle cx="46" cy="51" r="4.2" />
                <circle cx="32" cy="10" r="1.2" class="plan-tier-dot" />
                <circle cx="16" cy="22" r="1.1" class="plan-tier-dot" />
                <circle cx="48" cy="22" r="1.1" class="plan-tier-dot" />
                <circle cx="18" cy="51" r="1.1" class="plan-tier-dot" />
                <circle cx="46" cy="51" r="1.1" class="plan-tier-dot" />
              </g>

              <g v-else>
                <path d="M32 9v44M32 25 18 17M32 25l14-8M32 36 18 31M32 36l14-5M18 31 8 43M46 31l10 12M32 44 18 52M32 44l14 8" />
                <circle cx="32" cy="9" r="5" />
                <circle cx="18" cy="17" r="4" />
                <circle cx="46" cy="17" r="4" />
                <circle cx="18" cy="31" r="4" />
                <circle cx="46" cy="31" r="4" />
                <circle cx="8" cy="43" r="4.4" />
                <circle cx="56" cy="43" r="4.4" />
                <circle cx="18" cy="52" r="4" />
                <circle cx="46" cy="52" r="4" />
                <circle cx="32" cy="9" r="1.1" class="plan-tier-dot" />
                <circle cx="18" cy="17" r="1" class="plan-tier-dot" />
                <circle cx="46" cy="17" r="1" class="plan-tier-dot" />
                <circle cx="18" cy="31" r="1" class="plan-tier-dot" />
                <circle cx="46" cy="31" r="1" class="plan-tier-dot" />
                <circle cx="8" cy="43" r="1.1" class="plan-tier-dot" />
                <circle cx="56" cy="43" r="1.1" class="plan-tier-dot" />
                <circle cx="18" cy="52" r="1" class="plan-tier-dot" />
                <circle cx="46" cy="52" r="1" class="plan-tier-dot" />
              </g>
            </svg>
            <h3>{{ plan.name }}</h3>
            <p class="plan-subtitle">{{ plan.subtitle }}</p>
            <p class="plan-price">{{ plan.price }}</p>
            <p class="plan-cadence">{{ plan.cadence }}</p>

            <button class="plan-button" type="button">{{ plan.button }}</button>
            <p class="plan-note">{{ plan.note || '\u00a0' }}</p>

            <div class="plan-rule"></div>
            <p v-if="plan.intro" class="plan-intro">{{ plan.intro }}</p>
            <ul>
              <li v-for="feature in plan.features" :key="feature">{{ feature }}</li>
            </ul>
          </article>
        </div>

        <div v-else class="plans-grid plans-grid--team">
          <article v-for="plan in teamPlans" :key="plan.name" class="plan-card team-plan-card">
            <span class="plan-badge">{{ plan.badge }}</span>
            <div class="team-plan-icon" :class="`team-plan-icon--${plan.icon}`" aria-hidden="true">
              <span></span><span></span><span></span><span></span>
            </div>
            <h3>{{ plan.name }}</h3>
            <p class="plan-subtitle">{{ plan.subtitle }}</p>

            <div class="seat-box">
              <div v-for="tier in plan.tiers" :key="tier.name" class="seat-row">
                <div>
                  <strong>{{ tier.name }}</strong>
                  <p>{{ tier.description }}</p>
                  <small v-if="tier.note">{{ tier.note }}</small>
                </div>
                <span v-if="tier.price">{{ tier.price }}</span>
              </div>
            </div>

            <div class="plan-rule"></div>
            <p v-if="plan.intro" class="plan-intro">{{ plan.intro }}</p>
            <ul>
              <li v-for="feature in plan.features" :key="feature">{{ feature }}</li>
            </ul>

            <button class="plan-button team-plan-button" type="button">{{ plan.button }}</button>
          </article>
        </div>

        <p class="pricing-footnote">
          *Usage limits apply. Prices shown don't include applicable tax. Prices and plans are subject to change at Anthropic's discretion.
        </p>
      </section>

      <section class="faq-section" aria-labelledby="faq-heading">
        <h2 id="faq-heading">Frequently asked questions</h2>

        <div class="faq-list">
          <div v-for="(faq, index) in faqs" :key="faq.question" class="faq-item">
            <button type="button" @click="toggleFaq(index)">
              <span>{{ faq.question }}</span>
              <span class="faq-plus" aria-hidden="true">{{ openFaq === index ? '-' : '+' }}</span>
            </button>
            <p v-if="openFaq === index">{{ faq.answer }}</p>
          </div>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <div class="footer-brand">
        <a class="brand brand-light" href="#" aria-label="Claude home">
          <svg class="brand-mark" viewBox="0 0 100 100" aria-hidden="true">
            <path d="m19.6 66.5 19.7-11 .3-1-.3-.5h-1l-3.3-.2-11.2-.3L14 53l-9.5-.5-2.4-.5L0 49l.2-1.5 2-1.3 2.9.2 6.3.5 9.5.6 6.9.4L38 49.1h1.6l.2-.7-.5-.4-.4-.4L29 41l-10.6-7-5.6-4.1-3-2-1.5-2-.6-4.2 2.7-3 3.7.3.9.2 3.7 2.9 8 6.1L37 36l1.5 1.2.6-.4.1-.3-.7-1.1L33 25l-6-10.4-2.7-4.3-.7-2.6c-.3-1-.4-2-.4-3l3-4.2L28 0l4.2.6L33.8 2l2.6 6 4.1 9.3L47 29.9l2 3.8 1 3.4.3 1h.7v-.5l.5-7.2 1-8.7 1-11.2.3-3.2 1.6-3.8 3-2L61 2.6l2 2.9-.3 1.8-1.1 7.7L59 27.1l-1.5 8.2h.9l1-1.1 4.1-5.4 6.9-8.6 3-3.5L77 13l2.3-1.8h4.3l3.1 4.7-1.4 4.9-4.4 5.6-3.7 4.7-5.3 7.1-3.2 5.7.3.4h.7l12-2.6 6.4-1.1 7.6-1.3 3.5 1.6.4 1.6-1.4 3.4-8.2 2-9.6 2-14.3 3.3-.2.1.2.3 6.4.6 2.8.2h6.8l12.6 1 3.3 2 1.9 2.7-.3 2-5.1 2.6-6.8-1.6-16-3.8-5.4-1.3h-.8v.4l4.6 4.5 8.3 7.5L89 80.1l.5 2.4-1.3 2-1.4-.2-9.2-7-3.6-3-8-6.8h-.5v.7l1.8 2.7 9.8 14.7.5 4.5-.7 1.4-2.6 1-2.7-.6-5.8-8-6-9-4.7-8.2-.5.4-2.9 30.2-1.3 1.5-3 1.2-2.5-2-1.4-3 1.4-6.2 1.6-8 1.3-6.4 1.2-7.9.7-2.6v-.2H49L43 72l-9 12.3-7.2 7.6-1.7.7-3-1.5.3-2.8L24 86l10-12.8 6-7.9 4-4.6-.1-.5h-.3L17.2 77.4l-4.7.6-2-2 .2-3 1-1 8-5.5Z" />
          </svg>
          <span>Claude</span>
        </a>

        <div class="footer-legal">
          <strong>BY ANTHROPIC</strong>
          <span>&copy; 2026 ANTHROPIC PBC</span>
          <div class="socials" aria-label="Social links">
            <a href="#" aria-label="X">X</a>
            <a href="#" aria-label="Threads">@</a>
            <a href="#" aria-label="LinkedIn">in</a>
            <a href="#" aria-label="YouTube">YT</a>
            <a href="#" aria-label="Instagram">IG</a>
          </div>
        </div>
      </div>

      <nav class="footer-links" aria-label="Footer navigation">
        <div v-for="column in footerColumns" :key="column.heading" class="footer-column">
          <h3>{{ column.heading }}</h3>
          <a v-for="link in column.links" :key="link" href="#">{{ link }}</a>
        </div>
      </nav>
    </footer>
  </div>
</template>
