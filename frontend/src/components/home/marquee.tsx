import { Marquee } from "@/components/ui/marquee";
import Icons from "@/components/global/icons";
import Container from "../global/container";

const MARQUEE_ITEMS = [
    "Assess Water Quality",
    "Detect Algae Blooms",
    "Identify Unsafe Waters",
    "Real-time Predictions",
    "Marine Life Sustainability",
    "Smart Monitoring"
];


const MarqueeSlide = () => {
  return (
    <Container>
      <div className="w-full bg-primary py-4 overflow-hidden">
        <Marquee className="[--duration:20s] [--gap:2rem" pauseOnHover>
          <div className="flex items-center">
            {MARQUEE_ITEMS.map((item, index) => (
              <div key={index} className="flex items-center gap-x-4">
                <span className="text-base font-medium text-primary-foreground hover:opacity-70 transition-opacity">
                  {item}
                </span>
                <Icons.stars className="size-5 text-black mr-4" />
              </div>
            ))}
          </div>
        </Marquee>
      </div>
    </Container>
  );
}

export default MarqueeSlide;