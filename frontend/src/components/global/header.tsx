import Container from "./container";
import { ReturnButton } from "./return-button";

interface HeaderProps {
  title: string;
  description: string;
}

export function Header({ title, description }: HeaderProps) {
  return (
    <div className="relative mb-8 space-y-0 sm:mb-10">
      <Container className="w-full">
        <div className="flex items-start justify-between gap-3 sm:items-center sm:gap-4">
          <h1 className="min-w-0 max-w-2xl font-heading text-3xl font-semibold tracking-tight md:text-4xl">
            {title}
          </h1>
          <ReturnButton className="shrink-0" />
        </div>
      </Container>
      <Container delay={0.1} className="w-full">
        <p className="mt-3 max-w-2xl text-pretty text-muted-foreground sm:mt-4">
          {description}
        </p>
      </Container>
    </div>
  );
}
