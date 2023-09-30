#include <vcclr.h>

#include <mamba/core/activation.hpp>
#include <mamba/core/context.hpp>

auto Script(const std::string& s) {
  return gcnew System::String(s.c_str());
}

auto BuildActivate(std::wstring_view wsv, bool stack) {
  mamba::Context ctx;
  mamba::PowerShellActivator activator{ctx};
  if (wsv == L"base") {
    return activator.activate(ctx.prefix_params.root_prefix, stack);
  }
  if (wsv.find_first_of(L"/\\") != std::wstring::npos) {
    std::filesystem::path prefix{wsv};
    return activator.activate(prefix, stack);
  }
  fs::u8path candidate;
  for (const auto& dir : ctx.envs_dirs) {
    candidate = dir / wsv;
    if (fs::is_directory(candidate)) {
      return activator.activate(candidate, stack);
    }
  }
  auto message = fmt::format("Cannot activate, prefix does not exist at: {}",
                             ctx.envs_dirs[0] / wsv);
  throw gcnew System::Exception(Script(message));
}

public ref class Mamba {
 public:
  static auto Activate(System::String^ prefix_or_name, bool stack) {
    pin_ptr<const wchar_t> wch = PtrToStringChars(prefix_or_name);
    return Script(BuildActivate(wch, stack));
  }

  static auto Activate(System::String^ prefix_or_name) {
    return Activate(prefix_or_name, false);
  }

  static auto Activate(bool stack) {
    return Script(BuildActivate(L"base", stack));
  }

  static auto Activate() {
    return Activate(false);
  }

  static auto Reactivate() {
    mamba::Context ctx;
    mamba::PowerShellActivator activator{ctx};
    return Script(activator.reactivate());
  }

  static auto Deactivate() {
    mamba::Context ctx;
    mamba::PowerShellActivator activator{ctx};
    return Script(activator.deactivate());
  }

 private:
  Mamba() {}
  ~Mamba() {}
};
