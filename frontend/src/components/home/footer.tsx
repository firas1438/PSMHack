import Image from 'next/image';
import Link from 'next/link';
import Container from "../global/container";
import Wrapper from "../global/wrapper";
import { Mail } from "lucide-react";

const Footer = () => {
    const quickLinks = [
        { label: "Home", href: "/#hero" },
        { label: "Features", href: "/#features" },
        { label: "FAQ", href: "/#faq" },
        { label: "Get Started", href: "/#cta" },
    ];

    return (
      <footer className="relative pt-12 pb-8 w-full overflow-hidden border-t border-border/40">
        <Wrapper>
          <div className="grid gap-12 xl:grid-cols-2">
            {/* left side */}
            <Container animation="fadeRight" delay={0.4}>
              <div className="flex flex-col items-center md:items-start justify-start text-center md:text-left">
                <div className="flex items-center gap-2">
                  <Image src="/icons/icon.svg" alt="Logo" width={32} height={32} className="size-6" />
                  <span className="text-md lg:text-lg font-medium">
                    Aqualog
                  </span>
                </div>
                <p className="text-muted-foreground mt-4 text-sm max-w-xs">
                  AI for seawater livability and algae detection along protected coastal regions.
                </p>
              </div>
            </Container>

            {/* right side */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 w-full items-start justify-items-center md:justify-items-end">
              <Container
                animation="fadeUp"
                delay={0.5}
                className="flex flex-col items-center md:items-start"
              >
                <h3 className="text-base font-medium">Quick Links</h3>
                <ul className="mt-4 space-y-2 text-sm text-muted-foreground text-center md:text-left">
                  {quickLinks.map((link, index) => (
                    <li key={index}>
                      <Link
                        href={link.href}
                        className="hover:text-foreground transition-colors"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </Container>

              <Container
                animation="fadeUp"
                delay={0.5}
                className="flex flex-col items-center md:items-start"
              >
                <h3 className="text-base font-medium">Contact</h3>
                <div className="mt-4 flex items-center gap-2 text-sm text-muted-foreground">
                  <Mail className="size-4 text-primary shrink-0" />
                  <a
                    href="mailto:contact.aqualog@gmail.com"
                    className="hover:text-foreground transition-colors break-all"
                  >
                    contact.aqualog@gmail.com
                  </a>
                </div>
              </Container>
            </div>
          </div>

          <Container animation="fadeUp" delay={1}>
            <div className="mt-12 border-t border-border/80 pt-8 flex items-center justify-center">
              <p className="text-sm text-muted-foreground">
                © {new Date().getFullYear()} Aqualog. All rights reserved.
              </p>
            </div>
          </Container>
        </Wrapper>
      </footer>
    );
};

export default Footer;