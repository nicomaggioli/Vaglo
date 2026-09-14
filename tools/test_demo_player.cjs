const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const source = fs.readFileSync(path.join(__dirname, "../app.js"), "utf8");

function player({ readyState = 0, reducedMotion = false } = {}) {
  class Element extends EventTarget {
    constructor(dataset = {}) {
      super();
      this.dataset = dataset;
      this.focused = false;
    }
    click() {
      this.dispatchEvent(new Event("click"));
    }
    focus() {
      this.focused = true;
    }
    querySelectorAll() {
      return [];
    }
  }
  const openers = [new Element(), new Element({ start: "31.199" })];
  const chapters = [
    new Element({ time: "17.743" }),
    new Element({ time: "184.482" }),
  ];
  const closeButton = new Element();
  const video = Object.assign(new Element(), {
    readyState,
    currentTime: 0,
    plays: 0,
    pauses: 0,
    play() {
      this.plays += 1;
      return Promise.resolve();
    },
    pause() {
      this.pauses += 1;
    },
  });
  const dialog = Object.assign(new Element(), {
    open: false,
    scrolls: [],
    showModal() {
      this.open = true;
    },
    close() {
      this.open = false;
      this.dispatchEvent(new Event("close"));
    },
    scrollTo(options) {
      this.scrolls.push(options);
    },
    querySelector() {
      return closeButton;
    },
    querySelectorAll() {
      return chapters;
    },
  });
  const classes = new Set();
  const selectors = {
    "#mobile-menu": new Element(),
    "#trailer-dialog": dialog,
    "#full-video": video,
  };
  const document = Object.assign(new Element(), {
    body: {
      classList: {
        add: (name) => classes.add(name),
        remove: (name) => classes.delete(name),
      },
    },
    querySelector: (selector) => selectors[selector] || null,
    querySelectorAll: (selector) =>
      selector === "[data-trailer]" ? openers : [],
  });
  const matchMedia = () => ({ matches: reducedMotion, addEventListener() {} });
  vm.runInNewContext(source, {
    document,
    window: { scrollY: 0, addEventListener() {}, matchMedia },
    matchMedia,
  });
  const metadata = () => {
    video.readyState = 1;
    video.dispatchEvent(new Event("loadedmetadata"));
  };
  return { openers, chapters, closeButton, video, dialog, classes, metadata };
}

test("closing during the first load cannot restart hidden playback", () => {
  const p = player();
  p.openers[1].click();
  assert.equal(p.video.plays, 1, "loading begins in the click gesture");
  p.closeButton.click();
  const playsBeforeMetadata = p.video.plays;
  p.metadata();
  assert.equal(p.video.plays, playsBeforeMetadata);
  assert.equal(p.video.currentTime, 0);
  assert.equal(p.dialog.open, false);
  assert.equal(p.openers[1].focused, true);
  assert.equal(p.classes.has("modal-open"), false);
});

test("native dialog closure also cancels a pending seek", () => {
  const p = player();
  p.openers[1].click();
  p.dialog.close();
  p.metadata();
  assert.equal(p.video.plays, 1);
  assert.equal(p.video.currentTime, 0);
  assert.ok(p.video.pauses > 0);
});

test("only the latest chapter request runs when metadata arrives", () => {
  const p = player();
  p.openers[1].click();
  p.chapters[0].click();
  p.chapters[1].click();
  const playsBeforeMetadata = p.video.plays;
  p.metadata();
  assert.equal(p.video.plays, playsBeforeMetadata + 1);
  assert.equal(p.video.currentTime, 184.482);
  assert.equal(p.dialog.scrolls.at(-1).top, 0);
  assert.equal(p.dialog.scrolls.at(-1).behavior, "smooth");
});

test("reopening before metadata uses the new opener and cancels the old request", () => {
  const p = player();
  p.openers[1].click();
  p.dialog.close();
  p.openers[0].click();
  const playsBeforeMetadata = p.video.plays;
  p.metadata();
  assert.equal(p.video.currentTime, 0);
  assert.equal(p.video.plays, playsBeforeMetadata + 1);
  assert.equal(p.dialog.scrolls.at(-1).behavior, "instant");
});

test("loaded video seeks immediately and honors reduced motion", () => {
  const p = player({ readyState: 1, reducedMotion: true });
  p.openers[1].click();
  assert.equal(p.video.currentTime, 31.199);
  assert.equal(p.video.plays, 1);
  p.chapters[1].click();
  assert.equal(p.video.currentTime, 184.482);
  assert.equal(p.dialog.scrolls.at(-1).behavior, "auto");
  p.dialog.close();
  p.openers[0].click();
  assert.equal(p.video.currentTime, 0);
});
