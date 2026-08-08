import React, { useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import {
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  Check,
  ChevronRight,
  Database,
  Globe2,
  GraduationCap,
  Layers3,
  MapPinHouse,
  MessageCircle,
  PanelsTopLeft,
  Send,
  ShoppingBag,
  Sparkles,
  Store,
  UserRound,
  Workflow,
} from 'lucide-react'
import { SITE_CONFIG } from './config'
import './styles.css'

const services = [
  {
    icon: Send,
    title: 'Telegram-боты',
    description: 'Боты для заявок, записи, каталогов, консультаций и автоматизации.',
    price: SITE_CONFIG.prices.telegramBot,
    code: 'BOT / 01',
  },
  {
    icon: PanelsTopLeft,
    title: 'Сайт-визитка',
    description: 'Компактный современный сайт для специалиста или бизнеса.',
    price: SITE_CONFIG.prices.businessCard,
    code: 'WEB / 02',
  },
  {
    icon: Globe2,
    title: 'Лендинг',
    description: 'Продающая одностраничная страница под услугу или продукт.',
    price: SITE_CONFIG.prices.landing,
    code: 'PAGE / 03',
  },
  {
    icon: Workflow,
    title: 'Автоматизация',
    description: 'Интеграции, уведомления, формы, базы данных и нестандартные сценарии.',
    price: SITE_CONFIG.prices.automation,
    code: 'FLOW / 04',
  },
]

const audiences = [
  { icon: Store, label: 'Малый бизнес' },
  { icon: GraduationCap, label: 'Эксперты' },
  { icon: UserRound, label: 'Мастера и специалисты' },
  { icon: ShoppingBag, label: 'Интернет-магазины' },
  { icon: MapPinHouse, label: 'Локальные услуги' },
  { icon: Layers3, label: 'Онлайн-проекты' },
]

const projects = [
  {
    title: 'Telegram-бот для салона красоты',
    functions: ['Услуги', 'Запись', 'Заявки', 'Уведомления'],
    visual: 'calendar',
  },
  {
    title: 'Telegram-бот для приёма заявок',
    functions: ['Анкета', 'База заявок', 'Уведомление администратору'],
    visual: 'form',
  },
  {
    title: 'Telegram-бот с каталогом',
    functions: ['Категории', 'Карточки товаров', 'Заявки'],
    visual: 'catalog',
  },
  {
    title: 'Сайт-визитка специалиста',
    functions: ['Услуги', 'Цены', 'FAQ', 'Форма заявки'],
    visual: 'website',
  },
  {
    title: 'LUMÉ Beauty',
    type: 'Telegram-бот для салона красоты',
    description: 'Telegram-бот для автоматизации записи клиентов в салон красоты.',
    functions: [
      'Каталог услуг',
      'Выбор мастера',
      'Выбор даты и времени',
      'Подтверждение записи',
      'Раздел «Мои записи»',
      'Уведомления администратору',
      'Статистика',
      'Защита от двойного бронирования',
    ],
    details: 'Клиент самостоятельно выбирает услугу, мастера и свободное время, оставляет контакты и получает подтверждение записи. Все данные сохраняются, а администратор получает уведомление в Telegram.',
    visual: 'lume',
    featured: true,
  },
  {
    title: 'NOVA Store',
    type: 'Telegram-бот для интернет-магазина',
    description: 'Telegram-магазин с каталогом товаров, корзиной и оформлением заказа.',
    functions: [
      '3 категории товаров',
      '12 демонстрационных товаров',
      'Карточки товаров',
      'Корзина',
      'Изменение количества',
      'Удаление товаров',
      'Оформление заказа',
      'Доставка или самовывоз',
      'Раздел «Мои заказы»',
      'Уведомления администратору',
      'Административная статистика',
    ],
    details: 'Пользователь выбирает товары, добавляет их в корзину, меняет количество, выбирает способ получения и подтверждает заказ. После оформления заказ сохраняется, клиент получает номер заказа, а администратор — подробное уведомление в Telegram.',
    visual: 'nova',
    featured: true,
  },
  {
    title: 'ELENA MOROZOVA',
    type: 'Сайт-визитка частного специалиста',
    description: 'Современный адаптивный сайт-визитка психолога-консультанта с услугами, ценами, FAQ и формой заявки.',
    functions: [
      'Адаптивный дизайн',
      'Первый продающий экран',
      'Направления работы',
      'Услуги и цены',
      'Этапы работы',
      'FAQ',
      'Форма заявки',
      'Telegram и телефон',
      'SEO-метаданные',
    ],
    details: 'Демонстрационный сайт для частного специалиста. Проект показывает, как можно компактно представить услуги, стоимость, формат работы и контакты и привести посетителя к заявке.',
    demoUrl: 'https://elena-morozova-demo-production.up.railway.app',
    visual: 'elena',
    featured: true,
  },
]

const process = [
  'Вы описываете задачу.',
  'Я задаю уточняющие вопросы.',
  'Согласовываем стоимость и сроки.',
  'Я создаю проект.',
  'Вы проверяете результат.',
  'Вношу согласованные правки.',
  'Запускаем готовый проект.',
]

const benefits = [
  'Работа напрямую без менеджеров',
  'Понятное общение без сложной технической терминологии',
  'Быстрый запуск первой рабочей версии',
  'Разработка под конкретную задачу',
  'Возможность дальнейших доработок',
]

const prices = [
  ['Telegram-бот', SITE_CONFIG.prices.telegramBot],
  ['Сайт-визитка', SITE_CONFIG.prices.businessCard],
  ['Лендинг', SITE_CONFIG.prices.landing],
  ['Индивидуальная автоматизация', `цена ${SITE_CONFIG.prices.automation}`],
]

const faq = [
  ['Сколько занимает разработка?', 'Простой проект обычно можно собрать за несколько дней. Точный срок зависит от функций.'],
  ['Можно ли внести правки?', 'Да. Согласованный объём правок входит в работу.'],
  ['Что нужно от меня для начала?', 'Кратко описать задачу, желаемый результат и примеры, если они есть.'],
  ['Нужно ли мне разбираться в программировании?', 'Нет. Я объясню, как пользоваться готовым проектом.'],
  ['Можно ли потом доработать проект?', 'Да, функциональность можно расширять после запуска.'],
]

function Brand() {
  return (
    <a className="brand light" href="#top" aria-label={`${SITE_CONFIG.brand.name} — наверх`}>
      <img src={SITE_CONFIG.brand.avatar} alt="" width="42" height="42" loading="eager" decoding="async" fetchPriority="high" />
      <span className="brand-name" translate="no">{SITE_CONFIG.brand.name}</span>
      <i aria-hidden="true" />
    </a>
  )
}

function Header() {
  return (
    <header className="site-header">
      <Brand />
      <nav className="main-nav" aria-label="Основная навигация">
        <a href="#services">Услуги</a>
        <a href="#portfolio">Работы</a>
        <a href="#process">Процесс</a>
      </nav>
      <div className="availability"><i aria-hidden="true" /> Открыт для проектов</div>
    </header>
  )
}

function Hero() {
  return (
    <section className="hero-one" aria-labelledby="hero-title">
      <div className="eyebrow"><Sparkles aria-hidden="true" /> DIGITAL DEVELOPMENT · 2026</div>
      <h1 id="hero-title">Telegram-боты <span>и сайты</span><br />для вашего бизнеса</h1>
      <div className="one-bottom">
        <p>Автоматизирую заявки, продажи и рутину.<br />От идеи до работающего проекта.</p>
        <div className="actions dark">
          <a className="primary" href={SITE_CONFIG.telegram.url} target="_blank" rel="noreferrer">
            Обсудить проект <ArrowRight aria-hidden="true" />
          </a>
          <a className="secondary" href="#portfolio">
            Посмотреть работы <ArrowDownRight aria-hidden="true" />
          </a>
        </div>
      </div>
    </section>
  )
}

function SectionHeader({ number, eyebrow, title, description }) {
  return (
    <header className="section-header" data-reveal>
      <div className="section-index">/{number}</div>
      <div>
        <div className="section-eyebrow">{eyebrow}</div>
        <h2>{title}</h2>
        {description && <p>{description}</p>}
      </div>
    </header>
  )
}

function ServiceCard({ service, index }) {
  const Icon = service.icon
  return (
    <article className="service-card" data-reveal style={{ '--delay': `${index * 70}ms` }}>
      <div className="card-top"><span>{service.code}</span><Icon aria-hidden="true" /></div>
      <div>
        <h3>{service.title}</h3>
        <p>{service.description}</p>
      </div>
      <div className="card-price"><span>Стоимость</span><strong>{service.price}</strong></div>
    </article>
  )
}

function Services() {
  return (
    <section className="page-section" id="services">
      <SectionHeader number="01" eyebrow="Что можно разработать" title="Услуги" description="Собираю понятные цифровые инструменты под реальную задачу бизнеса." />
      <div className="services-grid">{services.map((service, index) => <ServiceCard key={service.title} service={service} index={index} />)}</div>
    </section>
  )
}

function Audience() {
  return (
    <section className="page-section audience-section" id="audience">
      <SectionHeader number="02" eyebrow="Кому это подходит" title="Для кого я работаю" />
      <div className="audience-grid" data-reveal>
        <div className="audience-core">
          <div className="core-orbit" aria-hidden="true"><i /><i /><i /></div>
          <span>Проекты для</span>
          <strong>людей<br />и бизнеса</strong>
        </div>
        <ul>
          {audiences.map(({ icon: Icon, label }, index) => (
            <li key={label}><span>0{index + 1}</span><Icon aria-hidden="true" /><strong>{label}</strong></li>
          ))}
        </ul>
      </div>
    </section>
  )
}

function ProjectVisual({ type }) {
  if (type === 'calendar') return <div className="visual calendar-ui" aria-hidden="true"><div className="ui-bar"><i /><i /><i /></div><div className="ui-title"><span>Запись на услугу</span><b>Выберите время</b></div><div className="date-row"><i>12</i><i className="active">13</i><i>14</i><i>15</i></div><div className="slot-row"><span>10:00</span><span>12:30</span><span>16:00</span></div></div>
  if (type === 'form') return <div className="visual form-ui" aria-hidden="true"><div className="ui-bar"><i /><i /><i /></div><div className="form-line"><span>01</span><b>Как к вам обращаться?</b><i /></div><div className="form-line active"><span>02</span><b>Опишите задачу</b><i /></div><div className="form-line"><span>03</span><b>Контакт для связи</b><i /></div><div className="progress-line"><i /></div></div>
  if (type === 'catalog') return <div className="visual catalog-ui" aria-hidden="true"><div className="ui-bar"><i /><i /><i /></div><div className="catalog-tabs"><span className="active">Все</span><span>Популярное</span><span>Новинки</span></div><div className="catalog-cards"><i /><i /><i /></div><div className="catalog-info"><b>Каталог</b><span>Выберите категорию →</span></div></div>
  if (type === 'lume') return <div className="visual lume-ui" aria-hidden="true"><div className="ui-bar"><i /><i /><i /></div><div className="lume-mark"><span>LUMÉ</span><b>BEAUTY</b></div><div className="lume-flow"><span>Услуга</span><i /><span>Мастер</span><i /><span>Время</span><i /><span>Готово</span></div></div>
  if (type === 'nova') return <div className="visual lume-ui nova-ui" aria-hidden="true"><div className="ui-bar"><i /><i /><i /></div><div className="lume-mark nova-mark"><span>NOVA</span><b>STORE</b></div><div className="lume-flow"><span>Каталог</span><i /><span>Корзина</span><i /><span>Доставка</span><i /><span>Заказ</span></div></div>
  if (type === 'elena') return <div className="visual elena-ui" aria-hidden="true"><div className="elena-browser"><div className="elena-browser-bar"><span><i /><i /><i /></span><b>elena-morozova.demo</b><em>WEB</em></div><div className="elena-page"><div className="elena-copy"><span>ПСИХОЛОГ-КОНСУЛЬТАНТ</span><strong>Спокойный формат<br />для важного разговора</strong><i /></div><div className="elena-panel"><span>Услуги</span><span>Форматы</span><span>FAQ</span><b>Записаться</b></div></div></div></div>
  return <div className="visual website-ui" aria-hidden="true"><div className="browser-bar"><i /><span>portfolio.site</span><i /></div><div className="website-copy"><span>СПЕЦИАЛИСТ</span><b>Помогаю решить<br />вашу задачу</b><i /></div><div className="website-side"><i /><i /><i /></div></div>
}

function Portfolio() {
  return (
    <section className="page-section" id="portfolio">
      <SectionHeader number="03" eyebrow="Как это может выглядеть" title="Портфолио" description="Концепции показывают возможную логику и подачу. Каждый реальный проект собирается под свою задачу." />
      <div className="projects-grid">
        {projects.map((project, index) => (
          <article className={`project-card${project.featured ? ' featured-project' : ''}${project.visual === 'lume' ? ' lume-project' : ''}${project.visual === 'nova' ? ' nova-project' : ''}${project.visual === 'elena' ? ' elena-project' : ''}`} data-reveal style={{ '--delay': `${index * 80}ms` }} key={project.title}>
            <ProjectVisual type={project.visual} />
            <div className="project-meta">
              <span className="project-number">0{index + 1}</span>
            </div>
            <h3>{project.title}</h3>
            {project.type && <p className="project-type">{project.type}</p>}
            {project.description && <p className="project-description">{project.description}</p>}
            <ul className="tag-list" aria-label="Функции проекта">{project.functions.map(item => <li key={item}>{item}</li>)}</ul>
            {project.details && !project.demoUrl && (
              <details className="project-details">
                <summary>Подробнее <ChevronRight aria-hidden="true" /></summary>
                <p>{project.details}</p>
              </details>
            )}
            {project.details && project.demoUrl && (
              <div className="project-actions">
                <details className="project-details">
                  <summary>Подробнее <ChevronRight aria-hidden="true" /></summary>
                  <p>{project.details}</p>
                </details>
                <a className="project-demo-link" href={project.demoUrl} target="_blank" rel="noreferrer">
                  Открыть демо <ArrowUpRight aria-hidden="true" />
                </a>
              </div>
            )}
          </article>
        ))}
      </div>
    </section>
  )
}

function Process() {
  return (
    <section className="page-section" id="process">
      <SectionHeader number="04" eyebrow="От сообщения до запуска" title="Как проходит работа" description="Без лишних созвонов и непонятных этапов. Вы всегда знаете, что происходит с проектом." />
      <ol className="process-list" data-reveal>
        {process.map((step, index) => (
          <li key={step}>
            <span>{String(index + 1).padStart(2, '0')}</span>
            <p>{step}</p>
            <Check aria-hidden="true" />
          </li>
        ))}
      </ol>
    </section>
  )
}

function Benefits() {
  return (
    <section className="page-section benefits-section" id="benefits">
      <SectionHeader number="05" eyebrow="Спокойный рабочий процесс" title="Почему со мной удобно работать" />
      <div className="benefits-layout">
        <div className="benefit-statement" data-reveal><MessageCircle aria-hidden="true" /><p>Один контакт.<br />Понятные решения.<br /><span>Фокус на вашей задаче.</span></p></div>
        <ul className="benefits-list">
          {benefits.map((benefit, index) => <li key={benefit} data-reveal style={{ '--delay': `${index * 55}ms` }}><span><Check aria-hidden="true" /></span><p>{benefit}</p></li>)}
        </ul>
      </div>
    </section>
  )
}

function Pricing() {
  return (
    <section className="page-section" id="pricing">
      <SectionHeader number="06" eyebrow="Ориентиры до обсуждения" title="Цены" description="Точная стоимость зависит от функций и объёма проекта." />
      <div className="price-list" data-reveal>
        {prices.map(([name, price], index) => (
          <div className="price-row" key={name}>
            <span>0{index + 1}</span><h3>{name}</h3><strong>{price}</strong><ChevronRight aria-hidden="true" />
          </div>
        ))}
      </div>
      <div className="price-note" data-reveal><Database aria-hidden="true" /><span>Финальная смета фиксируется после уточнения задачи.</span></div>
    </section>
  )
}

function FAQ() {
  return (
    <section className="page-section" id="faq">
      <SectionHeader number="07" eyebrow="Коротко о важном" title="FAQ" />
      <div className="faq-list" data-reveal>
        {faq.map(([question, answer], index) => (
          <details key={question} name="faq">
            <summary><span>0{index + 1}</span><strong>{question}</strong><i aria-hidden="true" /></summary>
            <p>{answer}</p>
          </details>
        ))}
      </div>
    </section>
  )
}

function FinalCTA() {
  return (
    <section className="final-cta" id="contact" aria-labelledby="contact-title">
      <div className="cta-glow" aria-hidden="true" />
      <div className="eyebrow" data-reveal><Sparkles aria-hidden="true" /> ГОТОВЫ ОБСУДИТЬ ЗАДАЧУ?</div>
      <h2 id="contact-title" data-reveal>Есть идея?<br /><span>Давайте превратим её</span><br />в работающий проект.</h2>
      <div className="actions dark" data-reveal>
        <a className="primary" href={SITE_CONFIG.telegram.url} target="_blank" rel="noreferrer">Обсудить проект <ArrowUpRight aria-hidden="true" /></a>
        <a className="secondary" href={SITE_CONFIG.telegram.botUrl} target="_blank" rel="noreferrer">Открыть Telegram-бота <Send aria-hidden="true" /></a>
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer className="site-footer">
      <Brand />
      <nav aria-label="Контакты">
        <a href={SITE_CONFIG.telegram.url} target="_blank" rel="noreferrer">{SITE_CONFIG.telegram.label}<ArrowUpRight aria-hidden="true" /></a>
      </nav>
      <p>© 2026 {SITE_CONFIG.brand.name}</p>
    </footer>
  )
}

function App() {
  useEffect(() => {
    document.documentElement.style.colorScheme = 'dark'
    const elements = document.querySelectorAll('[data-reveal]')
    if (!('IntersectionObserver' in window)) {
      elements.forEach(element => element.classList.add('is-visible'))
      return undefined
    }
    const observer = new IntersectionObserver(
      entries => entries.forEach(entry => entry.isIntersecting && (entry.target.classList.add('is-visible'), observer.unobserve(entry.target))),
      { threshold: 0.12 },
    )
    elements.forEach(element => observer.observe(element))
    return () => observer.disconnect()
  }, [])

  return (
    <>
      <a className="skip-link" href="#main">К основному содержанию</a>
      <div className="site-shell" id="top">
        <div className="ambient-grid" aria-hidden="true" />
        <div className="hero-shell">
          <div className="hero-orbit" aria-hidden="true"><span /><span /><span /></div>
          <Header />
          <main id="main">
            <Hero />
            <div className="tech-line"><span>Telegram Bots</span><i /> <span>Websites</span><i /> <span>Automation</span><i /> <span>AI</span></div>
            <Services />
            <Audience />
            <Portfolio />
            <Process />
            <Benefits />
            <Pricing />
            <FAQ />
            <FinalCTA />
          </main>
          <Footer />
        </div>
      </div>
    </>
  )
}

createRoot(document.getElementById('root')).render(<App />)
