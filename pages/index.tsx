import type { NextPage } from 'next'
import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>PotatoSalad|Home</title>
        <meta name="description" content="Next Generation PJSekai Fanmade Chart Server and SNS" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href="localhost:3000">PotatoSalad!</a>
        </h1>

        <p className={styles.description}>
          Get started by posting your own charts with{' '}
          <code className={styles.code}>PaletteWorks Editor</code>
        </p>

        <div className={styles.grid}>
          <a href="https://nextjs.org/docs" className={styles.card}>
            <h2>Post &rarr;</h2>
            <p>Post your charts and results</p>
          </a>

          <a href="https://nextjs.org/learn" className={styles.card}>
            <h2>Play &rarr;</h2>
            <p>Play with the NEW PotatoSalad server by{' '}
            <code className={styles.code}>@sevenc7c</code>
            </p>
          </a>

          <a
            href="https://github.com/vercel/next.js/tree/canary/examples"
            className={styles.card}
          >
            <h2>Stages &rarr;</h2>
            <p>Discover Stages by other users.</p>
          </a>

          <a
            href="https://vercel.com/new?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
            className={styles.card}
          >
            <h2>Cooperate &rarr;</h2>
            <p>
              Cooperate with others to make a chart together.
            </p>
          </a>
        </div>
      </main>

      <footer className={styles.footer}>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Sponcered by{' '}
          <span className={styles.logo}>
            <Image src="/vercel.svg" alt="Vercel Logo" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  )
}

export default Home
