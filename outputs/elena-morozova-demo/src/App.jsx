import { useState } from 'react'
import {
  ArrowDown,
  ArrowUpRight,
  Check,
  Clock3,
  Menu,
  MessageCircle,
  Phone,
  X,
} from 'lucide-react'

const topics = [
  'Тревога и стресс',
  'Отношения',
  'Эмоциональное выгорание',
  'Сложные жизненные решения',
  'Самооценка',
  'Личные границы',
]

const formats = [
  { title: 'Индивидуальная консультация', duration: '60 минут', price: '3 000 ₽' },
  { title: 'Онлайн-консультация', duration: '60 минут', price: '3 000 ₽' },
  { title: 'Первая ознакомительная встреча', duration: '30 минут', price: '1 500 ₽' },
]

const process = [
  'Вы оставляете заявку.',
  'Мы уточняем запрос.',
  'Выбираем удобное время.',
  'Проходит консультация.',
  'При необходимости договариваемся о дальнейшей работе.',
]

const benefits = [
  'Онлайн-формат',
  'Понятная запись',
  'Удобная мобильная версия',
  'Конфиденциальность',
  'Спокойная коммуникация',
]

const faq = [
  {
    question: 'Как проходит первая консультация?',
    answer: 'Первая встреча помогает спокойно сформулировать запрос, обсудить ожидания и определить возможный формат дальнейшей работы.',
  },
  {
    question: 'Можно ли проводить встречи онлайн?',
    answer: 'Да. В демонстрационном проекте предусмотрен онлайн-формат по предварительной записи.',
  },
  {
    question: 'Сколько длится консультация?',
    answer: 'Основная консультация длится 60 минут, ознакомительная встреча — 30 минут.',
  },
  {
    question: 'Как перенести встречу?',
    answer: 'Свяжитесь удобным способом и заранее сообщите, что хотите выбрать другое время.',
  },
  {
    question: 'Как записаться?',
    answer: 'Заполните форму ниже. Это демонстрация интерфейса: реальная отправка данных не выполняется.',
  },
]

function SectionHeader({ label, title, text }) {
  return (
    <div className="section-heading">
      <p className="eyebrow">{label}</p>
      <h2>{title}</h2>
      {text && <p className="section-intro">{text}</p>}
    </div>
  )
}

function Header() {
  const [menuOpen, setMenuOpen] = useState(false)

  const closeMenu = () => setMenuOpen(false)

  return (
    <header className="site-header">
      <a className="brand" href="#top" aria-label="ELENA MOROZOVA — к началу страницы">
        <span>ELENA</span>
        <span>MOROZOVA</span>
      </a>
      <nav className={`site-nav ${menuOpen ? 'is-open' : ''}`} aria-label="Основная навигация">
        <a href="#about" onClick={closeMenu}>Обо мне</a>
        <a href="#topics" onClick={closeMenu}>Запросы</a>
        <a href="#formats" onClick={closeMenu}>Форматы</a>
        <a href="#faq" onClick={closeMenu}>FAQ</a>
        <a className="nav-cta" href="#request" onClick={closeMenu}>Записаться</a>
      </nav>
      <button
        className="menu-button"
        type="button"
        aria-label={menuOpen ? 'Закрыть меню' : 'Открыть меню'}
        aria-expanded={menuOpen}
        onClick={() => setMenuOpen((current) => !current)}
      >
        {menuOpen ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
      </button>
    </header>
  )
}

function App() {
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (event) => {
    event.preventDefault()
    event.currentTarget.reset()
    setSubmitted(true)
  }

  return (
    <>
      <a className="skip-link" href="#main">Перейти к содержанию</a>
      <div className="page-shell">
        <Header />

        <main id="main">
          <section className="hero" id="top">
            <div className="hero-copy">
              <p className="demo-badge"><span aria-hidden="true" /> Демонстрационный проект</p>
              <h1>Психологическая консультация <em>в спокойном и понятном формате</em></h1>
              <p className="hero-text">Помогаю разобраться в сложных жизненных ситуациях и найти понятные следующие шаги.</p>
              <div className="hero-actions">
                <a className="button button-primary" href="#request">Записаться на консультацию <ArrowUpRight aria-hidden="true" /></a>
                <a className="button button-secondary" href="#about">Узнать подробнее <ArrowDown aria-hidden="true" /></a>
              </div>
              <p className="hero-note">Персональная страница · Онлайн-формат · Демо</p>
            </div>

            <div className="hero-art" aria-hidden="true">
              <div className="conversation-arch arch-outer" />
              <div className="conversation-arch arch-inner" />
              <div className="art-card">
                <span>Пространство</span>
                <p>для внимательного разговора и ясных следующих шагов</p>
                <span className="art-signature">EM</span>
              </div>
            </div>
          </section>

          <section className="section about" id="about">
            <SectionHeader label="Обо мне" title="Внимательный диалог без лишней сложности" />
            <div className="about-layout">
              <p className="about-lead">ELENA MOROZOVA — вымышленный образ специалиста, созданный исключительно для демонстрации сайта-визитки.</p>
              <div className="about-copy">
                <p>В основе консультационного формата — спокойный разговор, бережное отношение к запросу и понятная организация встреч.</p>
                <p>На этой странице не указаны образование, квалификация или профессиональный опыт: все содержание является демонстрационным.</p>
              </div>
            </div>
          </section>

          <section className="section topics" id="topics">
            <SectionHeader
              label="С чем можно обратиться"
              title="Темы, о которых бывает важно поговорить"
              text="Карточки показывают, как на персональном сайте можно понятно представить направления работы специалиста."
            />
            <div className="topic-grid">
              {topics.map((topic, index) => (
                <article className="topic-card" key={topic}>
                  <span className="topic-number">0{index + 1}</span>
                  <h3>{topic}</h3>
                  <span className="topic-line" aria-hidden="true" />
                </article>
              ))}
            </div>
          </section>

          <section className="section formats" id="formats">
            <SectionHeader
              label="Форматы работы"
              title="Понятные условия до первой встречи"
              text="Все цены и форматы на этой странице демонстрационные."
            />
            <div className="format-grid">
              {formats.map((format, index) => (
                <article className={`format-card ${index === 1 ? 'format-card-featured' : ''}`} key={format.title}>
                  <div>
                    <p className="format-index">Формат 0{index + 1}</p>
                    <h3>{format.title}</h3>
                  </div>
                  <div className="format-meta">
                    <span><Clock3 aria-hidden="true" /> {format.duration}</span>
                    <strong>{format.price}</strong>
                  </div>
                  <a href="#request">Выбрать формат <ArrowUpRight aria-hidden="true" /></a>
                </article>
              ))}
            </div>
          </section>

          <section className="section process" id="process">
            <SectionHeader label="Как проходит работа" title="От заявки до консультации — 5 понятных шагов" />
            <ol className="process-list">
              {process.map((item, index) => (
                <li key={item}>
                  <span>{String(index + 1).padStart(2, '0')}</span>
                  <p>{item}</p>
                </li>
              ))}
            </ol>
          </section>

          <section className="section benefits" id="benefits">
            <div className="benefit-panel">
              <SectionHeader label="Почему удобно" title="Спокойный формат взаимодействия" />
              <ul className="benefit-list">
                {benefits.map((benefit) => (
                  <li key={benefit}><Check aria-hidden="true" /> {benefit}</li>
                ))}
              </ul>
              <p className="benefit-note">Информация не является медицинской рекомендацией и не содержит гарантий результата.</p>
            </div>
          </section>

          <section className="section faq" id="faq">
            <SectionHeader label="FAQ" title="Ответы перед записью" />
            <div className="faq-list">
              {faq.map((item, index) => (
                <details key={item.question}>
                  <summary>
                    <span>{String(index + 1).padStart(2, '0')}</span>
                    {item.question}
                    <span className="faq-plus" aria-hidden="true">+</span>
                  </summary>
                  <p>{item.answer}</p>
                </details>
              ))}
            </div>
          </section>

          <section className="section request" id="request">
            <div className="request-copy">
              <p className="eyebrow">Форма заявки</p>
              <h2>Давайте выберем удобное время для разговора</h2>
              <p>Заполните форму — это демонстрация frontend-сценария без реальной отправки данных.</p>
              <div className="request-mark" aria-hidden="true">EM</div>
            </div>
            <form className="request-form" onSubmit={handleSubmit}>
              <div className="field">
                <label htmlFor="name">Имя</label>
                <input id="name" name="name" type="text" autoComplete="name" placeholder="Например, Анна…" required />
              </div>
              <div className="field">
                <label htmlFor="contact">Telegram или телефон</label>
                <input id="contact" name="contact" type="text" autoComplete="off" placeholder="@username или +7 900…" required />
              </div>
              <div className="field">
                <label htmlFor="contact-method">Удобный способ связи</label>
                <select id="contact-method" name="contactMethod" defaultValue="" autoComplete="off" required>
                  <option value="" disabled>Выберите способ…</option>
                  <option value="telegram">Telegram</option>
                  <option value="phone">Телефон</option>
                </select>
              </div>
              <div className="field">
                <label htmlFor="comment">Комментарий</label>
                <textarea id="comment" name="comment" rows="4" autoComplete="off" placeholder="Кратко опишите запрос…" />
              </div>
              <button className="button button-primary form-submit" type="submit">Отправить заявку <ArrowUpRight aria-hidden="true" /></button>
              <p className={`form-status ${submitted ? 'is-visible' : ''}`} aria-live="polite">
                {submitted ? 'Спасибо! Заявка принята. Я свяжусь с вами для уточнения деталей.' : ''}
              </p>
            </form>
          </section>

          <section className="section contacts" id="contacts">
            <SectionHeader label="Контакты" title="Удобный способ связи" text="Все контакты ниже демонстрационные и не принадлежат реальному специалисту." />
            <div className="contact-grid">
              <a href="https://t.me/elena_demo" target="_blank" rel="noreferrer">
                <MessageCircle aria-hidden="true" />
                <span>Telegram</span>
                <strong>@elena_demo</strong>
                <ArrowUpRight className="contact-arrow" aria-hidden="true" />
              </a>
              <a href="tel:+79000000000">
                <Phone aria-hidden="true" />
                <span>Телефон</span>
                <strong>+7 900 000-00-00</strong>
                <ArrowUpRight className="contact-arrow" aria-hidden="true" />
              </a>
            </div>
          </section>
        </main>

        <footer className="site-footer">
          <a className="brand brand-footer" href="#top">
            <span>ELENA</span>
            <span>MOROZOVA</span>
          </a>
          <p>Демонстрационный проект</p>
          <p>© 2026</p>
        </footer>
      </div>
    </>
  )
}

export default App
