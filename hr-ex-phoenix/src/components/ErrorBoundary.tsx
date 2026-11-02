import { Component, type ErrorInfo, type ReactNode } from "react";

const TEXT = {
  en: {
    title: "Something went wrong",
    body: "This page hit an unexpected error. Reloading usually fixes it; your language and theme are kept.",
    reload: "Reload",
    details: "Technical details",
  },
  fa: {
    title: "مشکلی پیش آمد",
    body: "این صفحه با خطای غیرمنتظره‌ای روبه‌رو شد. معمولاً بارگذاری دوباره مشکل را حل می‌کند؛ زبان و پوسته حفظ می‌شوند.",
    reload: "بارگذاری دوباره",
    details: "جزئیات فنی",
  },
} as const;

function currentLang(): "en" | "fa" {
  try {
    if (localStorage.getItem("pp-lang") === "fa") return "fa";
  } catch { /* storage blocked */ }
  return document.documentElement.lang === "fa" ? "fa" : "en";
}

interface Props { children: ReactNode; onReload?: () => void }
interface State { error: Error | null }

/** Catches render errors anywhere below it and shows a bilingual fallback with a reload button. */
export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("[phoenix] render error", error, info.componentStack);
  }

  render() {
    const { error } = this.state;
    if (!error) return this.props.children;
    const lang = currentLang();
    const t = TEXT[lang];
    const reload = this.props.onReload ?? (() => window.location.reload());
    return (
      <div className="page error-boundary" role="alert" lang={lang} dir={lang === "fa" ? "rtl" : "ltr"}>
        <h1>{t.title}</h1>
        <p>{t.body}</p>
        <button type="button" className="eb-reload" onClick={reload}>{t.reload}</button>
        <details>
          <summary>{t.details}</summary>
          <pre dir="ltr" lang="en"><code>{String(error.message || error)}</code></pre>
        </details>
      </div>
    );
  }
}
